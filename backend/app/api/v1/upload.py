"""
File upload endpoint.
"""
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.content import ContentResponse
from app.services.content_service import ContentService

router = APIRouter()


@router.post("", response_model=ContentResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload image, audio, or video file."""
    service = ContentService(db)
    return await service.save_uploaded_file(file)
