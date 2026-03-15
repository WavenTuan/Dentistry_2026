"""
Content SQLAlchemy model.
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func

from app.core.database import Base


class ContentType(str, enum.Enum):
    text = "text"
    image = "image"
    audio = "audio"
    video = "video"


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ContentType), nullable=False)
    text_content = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    mime_type = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
