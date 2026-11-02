from datetime import datetime
from typing import Any

from app import db


class Page(db.Model):
    __tablename__ = "pages"

    id: Any = db.Column(db.Integer, primary_key=True)
    title: Any = db.Column(db.String(200), nullable=False)
    slug: Any = db.Column(db.String(200), unique=True, nullable=False, index=True)
    content: Any = db.Column(db.Text, nullable=False, default="")
    is_published: Any = db.Column(db.Boolean, default=False, nullable=False)
    created_at: Any = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: Any = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
