import os
from collections.abc import Callable
from functools import wraps
from typing import Any, TypedDict

import jwt
from flask import request

from .response import Response


class UserPayload(TypedDict, total=False):
    id: int
    username: str
    email: str


class JWTPayload(TypedDict, total=False):
    user: UserPayload
    exp: int | float


class Middleware:
    def __init__(self) -> None:
        pass

    @staticmethod
    def decode_auth_token(auth_token: str) -> dict[str, Any]:
        """Decode and validate a JWT token. Raises ValueError on failure."""
        jwt_key = os.getenv("JWT_KEY")
        if not jwt_key:
            raise ValueError("JWT_KEY is not configured")
        try:
            return jwt.decode(auth_token, jwt_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidSignatureError:
            raise ValueError("Token signature verification failed")
        except jwt.DecodeError:
            raise ValueError("Token is malformed or invalid")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")

    @staticmethod
    def token_required(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> Any:
            auth_header = request.headers.get("Authorization", "")
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response().invalid(
                    is_success=False,
                    values=None,
                    message="Authorization header missing or malformed. Use 'Bearer <token>'.",
                    code=401,
                )
            token = auth_header.split(" ", 1)[1].strip()
            if not token:
                return Response().invalid(
                    is_success=False,
                    values=None,
                    message="Token missing after Bearer prefix.",
                    code=401,
                )
            try:
                payload = Middleware.decode_auth_token(token)
                current_user = payload.get("user")
                if not current_user:
                    return Response().invalid(
                        is_success=False,
                        values=None,
                        message="Invalid token: missing 'user' payload",
                        code=401,
                    )
            except (ValueError, KeyError) as e:
                return Response().invalid(is_success=False, values=None, message=str(e), code=401)
            except Exception:
                return Response().invalid(
                    is_success=False,
                    values=None,
                    message="Unexpected token validation error",
                    code=401,
                )
            return f(*args, current_user=current_user, **kwargs)

        return decorated

    @staticmethod
    def role_required(allowed_roles: list[str]) -> Callable[..., Any]:
        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(f)
            def decorated(current_user: Any, *args: Any, **kwargs: Any) -> Any:
                role_name = getattr(getattr(current_user, "role", None), "name", "")
                if role_name.lower() not in [r.lower() for r in allowed_roles]:
                    return Response().invalid(
                        values=None,
                        message=f"Access Denied! Role `{role_name}` Not Allowed.",
                        code=403,
                    )
                return f(current_user, *args, **kwargs)

            return decorated

        return decorator
