"""
Content CRUD and list endpoints.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.content import ContentCreate, ContentResponse, ContentListResponse
from app.services.content_service import ContentService

router = APIRouter()


@router.post("", response_model=ContentResponse)
def create_content(data: ContentCreate, db: Session = Depends(get_db)):
    """Submit text content."""
    service = ContentService(db)
    return service.create_text_content(data.text_content)


@router.get("", response_model=ContentListResponse)
def list_contents(
    since: int | None = Query(None, description="Return items with id greater than this"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """List contents with optional cursor pagination."""
    service = ContentService(db)
    items = service.list_contents(since=since, limit=limit)
    return ContentListResponse(contents=items)
