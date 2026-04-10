import jwt
from flask import g, request
from functools import wraps
from utils import Response
import os

class Middleware:
    def __init__(self):
        pass

    @staticmethod
    def decode_auth_token(auth_token: str) -> dict:
        """Decode and validate a JWT token. Raises ValueError on failure."""
        try:
            return jwt.decode(auth_token, str(os.getenv("JWT_KEY")), algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header or not auth_header.startswith("Bearer "):
                return Response().invalid(
                    is_success=False, values=None,
                    message="Authorization header missing or malformed. Use 'Bearer <token>'.",
                    code=401,
                )
            try:
                token = auth_header.split(" ", 1)[1]
                payload = Middleware.decode_auth_token(token)
                current_user = payload["user"]
            except (ValueError, KeyError) as e:
                return Response().invalid(
                    is_success=False, values=None, message=str(e), code=401
                )
            return f(*args, current_user=current_user, **kwargs)

        return decorated

    @staticmethod
    def role_required(allowed_roles):
        def decorator(f):
            @wraps(f)
            def decorated(current_user, *args, **kwargs):
                if current_user.role.name.lower() not in allowed_roles:
                    return Response().invalid(
                        None,
                        f"Access Denied! Role `{current_user.role.name}` Not Allowed.",
                        403,
                    )
                return f(current_user, *args, **kwargs)

            return decorated

        return decorator
