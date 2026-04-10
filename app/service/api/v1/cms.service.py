from app.model.models import Page
from app import db


class CmsApiService:

    @staticmethod
    def list_pages(published_only: bool = False) -> list:
        q = Page.query
        if published_only:
            q = q.filter_by(is_published=True)
        return [p.to_dict() for p in q.order_by(Page.created_at.desc()).all()]

    @staticmethod
    def get_page(page_id: int):
        page = Page.query.get(page_id)
        return page.to_dict() if page else None

    @staticmethod
    def create_page(data: dict) -> dict:
        page = Page(
            title=data["title"],
            slug=data["slug"],
            content=data.get("content", ""),
            is_published=data.get("is_published", False),
        )
        db.session.add(page)
        db.session.commit()
        return page.to_dict()

    @staticmethod
    def update_page(page_id: int, data: dict):
        page = Page.query.get(page_id)
        if not page:
            return None
        if "title"        in data: page.title        = data["title"]
        if "slug"         in data: page.slug         = data["slug"]
        if "content"      in data: page.content      = data["content"]
        if "is_published" in data: page.is_published = data["is_published"]
        db.session.commit()
        return page.to_dict()

    @staticmethod
    def delete_page(page_id: int) -> bool:
        page = Page.query.get(page_id)
        if not page:
            return False
        db.session.delete(page)
        db.session.commit()
        return True
