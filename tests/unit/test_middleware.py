import os
from datetime import UTC, datetime, timedelta

import jwt
import pytest
from flask import Flask

from utils.middleware import Middleware
from utils.response import Response


@pytest.fixture
def test_app():
    app = Flask("middleware_test")
    app.config["JWT_KEY"] = "test-jwt-secret-key-for-testing-only"
    os.environ["JWT_KEY"] = "test-jwt-secret-key-for-testing-only"

    @app.route("/protected")
    @Middleware.token_required
    def protected_route(current_user):
        return Response().success(is_success=True, values=current_user, message="Access granted")

    return app


def test_token_required_missing_header(test_app):
    with test_app.test_client() as client:
        res = client.get("/protected")
        assert res.status_code == 401
        assert "Authorization header missing or malformed" in res.get_json()["message"]


def test_token_required_malformed_header(test_app):
    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": "Basic 12345"})
        assert res.status_code == 401
        assert "Authorization header missing or malformed" in res.get_json()["message"]


def test_token_required_empty_bearer(test_app):
    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": "Bearer "})
        assert res.status_code == 401
        assert "Token missing" in res.get_json()["message"]


def test_token_required_expired_token(test_app):
    jwt_key = os.environ["JWT_KEY"]
    expired_payload = {
        "user": {"id": 1, "username": "alice"},
        "exp": datetime.now(UTC) - timedelta(hours=1),
    }
    token = jwt.encode(expired_payload, jwt_key, algorithm="HS256")

    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 401
        assert "Token has expired" in res.get_json()["message"]


def test_token_required_invalid_signature(test_app):
    payload = {
        "user": {"id": 1, "username": "alice"},
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    token = jwt.encode(payload, "wrong-key-secret-that-does-not-match", algorithm="HS256")

    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 401
        assert (
            "signature" in res.get_json()["message"].lower()
            or "invalid" in res.get_json()["message"].lower()
        )


def test_token_required_missing_user_payload(test_app):
    jwt_key = os.environ["JWT_KEY"]
    payload = {
        "sub": "12345",
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    token = jwt.encode(payload, jwt_key, algorithm="HS256")

    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 401
        assert "user" in res.get_json()["message"].lower()


def test_token_required_valid_token(test_app):
    jwt_key = os.environ["JWT_KEY"]
    payload = {
        "user": {"id": 42, "username": "admin", "email": "admin@example.com"},
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }
    token = jwt.encode(payload, jwt_key, algorithm="HS256")

    with test_app.test_client() as client:
        res = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["id"] == 42
        assert data["data"]["username"] == "admin"
