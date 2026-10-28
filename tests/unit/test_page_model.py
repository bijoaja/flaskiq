from app.model.page import Page


def test_page_model_defaults(app, db):
    page = Page(title="About Us", slug="about-us")
    db.session.add(page)
    db.session.commit()

    saved = db.session.get(Page, page.id)
    assert saved is not None
    assert saved.title == "About Us"
    assert saved.slug == "about-us"
    assert saved.content == ""
    assert saved.is_published is False
    assert saved.created_at is not None
    assert saved.updated_at is not None


def test_page_to_dict(app, db):
    page = Page(title="Docs", slug="docs", content="Documentation content", is_published=True)
    db.session.add(page)
    db.session.commit()

    data = page.to_dict()
    assert data["id"] == page.id
    assert data["title"] == "Docs"
    assert data["slug"] == "docs"
    assert data["content"] == "Documentation content"
    assert data["is_published"] is True
    assert data["created_at"] is not None
    assert data["updated_at"] is not None
