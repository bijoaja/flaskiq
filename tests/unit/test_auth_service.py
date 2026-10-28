import os
import jwt
import pytest
from app.service.view.auth_service import AuthService


def test_auth_service_register_success(app, db):
    result = AuthService.register("bob", "bob@example.com", "secure123")

    assert result["id"] is not None
    assert result["username"] == "bob"
    assert result["email"] == "bob@example.com"


def test_auth_service_register_duplicate_email(app, db):
    AuthService.register("user1", "same@example.com", "pass123")

    with pytest.raises(ValueError, match="Email already registered"):
        AuthService.register("user2", "same@example.com", "pass456")


def test_auth_service_register_duplicate_username(app, db):
    AuthService.register("sameuser", "user1@example.com", "pass123")

    with pytest.raises(ValueError, match="Username already taken"):
        AuthService.register("sameuser", "user2@example.com", "pass456")


def test_auth_service_login_success_and_token_decode(app, db):
    AuthService.register("charlie", "charlie@example.com", "correctpass")

    token = AuthService.login("charlie@example.com", "correctpass")
    assert isinstance(token, str)

    jwt_key = os.getenv("JWT_KEY", "dev-secret")
    payload = jwt.decode(token, jwt_key, algorithms=["HS256"])

    assert "user" in payload
    assert payload["user"]["username"] == "charlie"
    assert payload["user"]["email"] == "charlie@example.com"
    assert "exp" in payload


def test_auth_service_login_invalid_password(app, db):
    AuthService.register("dave", "dave@example.com", "correctpass")

    with pytest.raises(ValueError, match="Invalid email or password"):
        AuthService.login("dave@example.com", "wrongpass")


def test_auth_service_login_nonexistent_user(app, db):
    with pytest.raises(ValueError, match="Invalid email or password"):
        AuthService.login("nonexistent@example.com", "anypass")
