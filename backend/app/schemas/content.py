"""
Pydantic schemas for content request/response.
"""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


ContentType = Literal["text", "image", "audio", "video"]


class ContentCreate(BaseModel):
    type: Literal["text"] = "text"
    text_content: str


class ContentResponse(BaseModel):
    id: int
    type: ContentType
    text_content: str | None = None
    file_url: str | None = None
    created_at: datetime
    reply_message: str | None = None  # 后端回复给前端的展示内容，如「我们医生组先想想」

    class Config:
        from_attributes = True


class ContentListResponse(BaseModel):
    contents: list[ContentResponse]
