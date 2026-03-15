"""
Data access layer for Content. Kept for future analytics/query extensions.
"""
from sqlalchemy.orm import Session

from app.models.content import Content


class ContentRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Content | None:
        return self.db.query(Content).filter(Content.id == id).first()

    def list_ids_after(self, since_id: int | None, limit: int):
        q = self.db.query(Content.id).order_by(Content.id.asc())
        if since_id is not None:
            q = q.filter(Content.id > since_id)
        return [r[0] for r in q.limit(limit).all()]
