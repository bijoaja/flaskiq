import os
from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from app.model.user import User
from app.repository.user_repository import UserRepository
from config import Config


class AuthService:
    @staticmethod
    def register(username: str, email: str, password: str) -> dict[str, Any]:
        if UserRepository.get_by_email(email):
            raise ValueError("Email already registered")
        if UserRepository.get_by_username(username):
            raise ValueError("Username already taken")
        user = UserRepository.create(username, email, password)
        return {"id": user.id, "username": user.username, "email": user.email}

    @staticmethod
    def login(email: str, password: str) -> str:
        user = UserRepository.get_by_email(email)
        if not user or not user.check_password(password):
            raise ValueError("Invalid email or password")
        return AuthService._generate_token(user)

    @staticmethod
    def _generate_token(user: User) -> str:
        expiry = datetime.now(UTC) + timedelta(minutes=int(os.getenv("JWT_EXPIRY_MINUTES", "60")))
        payload = {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            "exp": expiry,
        }
        jwt_key = os.getenv("JWT_KEY", Config.JWT_KEY)
        return jwt.encode(payload, jwt_key, algorithm=Config.JWT_ALGORITHM)
