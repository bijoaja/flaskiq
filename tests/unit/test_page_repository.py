from app.repository.page_repository import PageRepository


def test_page_repository_create_and_get(app, db):
    page_data = {
        "title": "Welcome",
        "slug": "welcome",
        "content": "Welcome to our site",
        "is_published": True,
    }
    page = PageRepository.create(page_data)

    assert page.id is not None
    assert page.title == "Welcome"

    found = PageRepository.get_by_slug("welcome")
    assert found is not None
    assert found.id == page.id

    all_pages = PageRepository.get_all()
    assert len(all_pages) == 1
    assert all_pages[0].id == page.id


def test_page_repository_get_by_slug_published_filter(app, db):
    PageRepository.create(
        {
            "title": "Draft",
            "slug": "draft-page",
            "content": "Draft content",
            "is_published": False,
        }
    )

    # Default is published_only=True
    assert PageRepository.get_by_slug("draft-page") is None
    # published_only=False finds draft
    assert PageRepository.get_by_slug("draft-page", published_only=False) is not None


def test_page_repository_update_and_delete(app, db):
    page = PageRepository.create(
        {
            "title": "Initial",
            "slug": "initial",
            "content": "Initial content",
            "is_published": False,
        }
    )

    updated = PageRepository.update(
        page.id,
        {
            "title": "Updated Title",
            "is_published": True,
        },
    )
    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.is_published is True

    # Update non-existent returns None
    assert PageRepository.update(9999, {"title": "Ghost"}) is None

    # Delete
    deleted = PageRepository.delete_by_id(page.id)
    assert deleted is True
    assert PageRepository.get_by_id(page.id) is None
    assert PageRepository.delete_by_id(page.id) is False
