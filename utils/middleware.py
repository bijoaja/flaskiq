import jwt
from flask import g, request
from functools import wraps
from utils import Response
import os

class Middleware:
    def __init__(self):
        pass

    @staticmethod
    def decode_auth_token(auth_token):
        """Memvalidasi token JWT."""
        try:
            payload = jwt.decode(
                auth_token, str(os.getenv("JWT_KEY")), algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return "Token expired."
        except jwt.InvalidTokenError as e:
            return f"Invalid token. {str(e)}"
        except Exception as e:
            return f"Token decoding error: {str(e)}"

    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")

            if not token:
                return Response().invalid(is_success=False, values=None, message="Token is missing! Please login.", code=401)

            try:
                # print(token)
                token = token.split(" ")[1]
                decode = Middleware.decode_auth_token(token)
                current_user = decode["user"]

                if not current_user:
                    return Response().invalid(is_success=False, values=None, message="User not found.", code=401)

            except Exception as e:
                return Response().invalid(is_success=False, values=None, message=f"Invalid token! {str(e)}", code=401)

            return f(
                *args, current_user=current_user, **kwargs
            )  # Kirim current_user ke endpoint

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
