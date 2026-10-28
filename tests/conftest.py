import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("JWT_KEY", "test-jwt-secret-key-for-testing-only")
os.environ.setdefault("WTF_CSRF_ENABLED", "False")

import pytest


@pytest.fixture
def app():
    from app import create_app, db

    application = create_app("testing")
    application.config["WTF_CSRF_ENABLED"] = False
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    from app import db as _db

    return _db
