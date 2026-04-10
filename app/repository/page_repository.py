from app import db
from app.repository.base_repository import BaseRepository
from app.model.page import Page


class PageRepository(BaseRepository):
    model = Page

    @classmethod
    def get_published(cls) -> list:
        return Page.query.filter_by(is_published=True).order_by(Page.created_at.desc()).all()

    @classmethod
    def get_by_slug(cls, slug: str, published_only: bool = True):
        query = Page.query.filter_by(slug=slug)
        if published_only:
            query = query.filter_by(is_published=True)
        return query.first()

    @classmethod
    def create(cls, data: dict) -> Page:
        page = Page(
            title=data["title"],
            slug=data["slug"],
            content=data.get("content", ""),
            is_published=data.get("is_published", False),
        )
        cls.save(page)
        return page

    @classmethod
    def update(cls, page_id: int, data: dict):
        page = cls.get_by_id(page_id)
        if not page:
            return None
        for field in ("title", "slug", "content", "is_published"):
            if field in data:
                setattr(page, field, data[field])
        db.session.commit()
        return page

    @classmethod
    def delete_by_id(cls, page_id: int) -> bool:
        page = cls.get_by_id(page_id)
        if not page:
            return False
        cls.delete(page)
        return True
