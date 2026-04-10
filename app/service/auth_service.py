import os
import jwt
from datetime import datetime, timedelta, timezone

from app.repository.user_repository import UserRepository


class AuthService:

    @staticmethod
    def register(username: str, email: str, password: str) -> dict:
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
    def _generate_token(user) -> str:
        expiry = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("JWT_EXPIRY_MINUTES", "60"))
        )
        payload = {
            "user": {
                "id":       user.id,
                "username": user.username,
                "email":    user.email,
            },
            "exp": expiry,
        }
        return jwt.encode(payload, os.getenv("JWT_KEY", "dev-secret"), algorithm="HS256")
