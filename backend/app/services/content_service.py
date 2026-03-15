"""
Content business logic: create text, save uploads, list contents.
"""
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.content import Content, ContentType
from app.schemas.content import ContentResponse

# Allowed MIME types per content type
UPLOAD_ALLOWED = {
    ContentType.image: {"image/jpeg", "image/png", "image/gif", "image/webp"},
    ContentType.audio: {"audio/mpeg", "audio/wav", "audio/ogg", "audio/webm", "audio/mp4"},
    ContentType.video: {"video/mp4", "video/webm", "video/ogg"},
}


REPLY_MESSAGE = "我们医生组先想想"


def _content_to_response(c: Content) -> ContentResponse:
    file_url = None
    if c.file_path:
        file_url = f"/api/v1/files/{c.file_path}"
    return ContentResponse(
        id=c.id,
        type=c.type.value,
        text_content=c.text_content,
        file_url=file_url,
        created_at=c.created_at,
        reply_message=REPLY_MESSAGE,
    )


class ContentService:
    def __init__(self, db: Session):
        self.db = db

    def create_text_content(self, text: str) -> ContentResponse:
        content = Content(
            type=ContentType.text,
            text_content=text.strip(),
        )
        self.db.add(content)
        self.db.commit()
        self.db.refresh(content)
        return _content_to_response(content)

    def list_contents(self, since: int | None = None, limit: int = 50) -> list[ContentResponse]:
        q = self.db.query(Content).order_by(Content.id.desc())
        if since is not None:
            q = q.filter(Content.id > since)
        rows = q.limit(limit).all()
        return [_content_to_response(c) for c in reversed(rows)]

    async def save_uploaded_file(self, file: UploadFile) -> ContentResponse:
        content_type = _infer_content_type(file.content_type, file.filename)
        if content_type is None:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Use image, audio, or video.",
            )

        settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        ext = Path(file.filename or "").suffix or _default_extension(content_type)
        safe_name = f"{uuid.uuid4().hex}{ext}"
        dest = settings.UPLOAD_DIR / safe_name

        content = await file.read()
        dest.write_bytes(content)

        record = Content(
            type=content_type,
            file_path=safe_name,
            mime_type=file.content_type,
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return _content_to_response(record)


def _infer_content_type(mime: str | None, filename: str | None) -> ContentType | None:
    mime = (mime or "").strip().lower()
    for ct, allowed in UPLOAD_ALLOWED.items():
        if mime in allowed:
            return ct
    # Fallback by extension
    ext = (Path(filename or "").suffix or "").lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return ContentType.image
    if ext in {".mp3", ".wav", ".ogg", ".webm", ".m4a"}:
        return ContentType.audio
    if ext in {".mp4", ".webm", ".ogv"}:
        return ContentType.video
    return None


def _default_extension(ct: ContentType) -> str:
    if ct == ContentType.image:
        return ".png"
    if ct == ContentType.audio:
        return ".mp3"
    return ".mp4"
