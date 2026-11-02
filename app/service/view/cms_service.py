from typing import Any

from app.model.page import Page
from app.repository.page_repository import PageRepository


class CmsService:
    """Unified CMS service used by both view controllers and API controllers."""

    @staticmethod
    def get_published_pages() -> list[Page]:
        return PageRepository.get_published()

    @staticmethod
    def get_page_by_slug(slug: str) -> Page | None:
        return PageRepository.get_by_slug(slug, published_only=True)

    @staticmethod
    def list_pages(published_only: bool = False) -> list[dict[str, Any]]:
        pages = PageRepository.get_published() if published_only else PageRepository.get_all()
        return [p.to_dict() for p in pages]

    @staticmethod
    def get_page(page_id: int) -> dict[str, Any] | None:
        page = PageRepository.get_by_id(page_id)
        return page.to_dict() if page else None

    @staticmethod
    def create_page(data: dict[str, Any]) -> dict[str, Any]:
        page = PageRepository.create(data)
        return page.to_dict()

    @staticmethod
    def update_page(page_id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        page = PageRepository.update(page_id, data)
        return page.to_dict() if page else None

    @staticmethod
    def delete_page(page_id: int) -> bool:
        return PageRepository.delete_by_id(page_id)
