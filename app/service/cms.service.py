from app.model.models import Page


class CmsService:
    @staticmethod
    def get_published_pages() -> list:
        return Page.query.filter_by(is_published=True).order_by(Page.created_at.desc()).all()

    @staticmethod
    def get_page_by_slug(slug: str):
        return Page.query.filter_by(slug=slug, is_published=True).first()
