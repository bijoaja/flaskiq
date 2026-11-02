"""
Profiler — request timing utility.

App-wide (automatic):
    Profiler.register_profiler(app)

Per-function (decorator):
    @Profiler.track
    def expensive_operation():
        ...

Read identity in a request context:
    identity = Profiler.get_identity()   # "user:42" or "ip:127.0.0.1"
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from flask import g, request

logger = logging.getLogger("flaskiq.profiler")


def _resolve_identity() -> str:
    """Return a short identity string for the current request.

    Authenticated requests → "user:<id>"
    Anonymous requests     → "ip:<remote_addr>"

    Decodes JWT inline to avoid circular imports with the rest of utils.
    """
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            import os

            import jwt

            token = auth_header.split(" ", 1)[1].strip()
            jwt_key = os.getenv("JWT_KEY", "")
            if token and jwt_key:
                payload = jwt.decode(token, jwt_key, algorithms=["HS256"])
                user_id = payload.get("user", {}).get("id")
                if user_id:
                    return f"user:{user_id}"
        except (jwt.PyJWTError, KeyError, ValueError, AttributeError) as exc:
            logger.debug("Failed to resolve identity from token: %s", exc)
    return f"ip:{request.remote_addr}"


class Profiler:
    @staticmethod
    def register_profiler(app: Any) -> None:
        """Register before/after hooks to log every request duration."""

        @app.before_request
        def _start_timer() -> None:
            g.start_time = time.perf_counter()

        @app.after_request
        def _log_request(response: Any) -> Any:
            if hasattr(g, "start_time"):
                duration = time.perf_counter() - g.start_time
                identity = _resolve_identity()
                logger.info(
                    "[%s] %s %s -> %d  %.4fs",
                    identity,
                    request.method,
                    request.path,
                    response.status_code,
                    duration,
                )
            return response

    @staticmethod
    def track(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator — logs execution time of any function.

        Works inside and outside a request context.

        Example::

            @Profiler.track
            def send_email(to):
                ...
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            logger.info("[track] %s  %.4fs", func.__qualname__, duration)
            return result

        return wrapper

    @staticmethod
    def get_identity() -> str:
        """Return the identity string for the current request.

        Safe to call anywhere inside a request context.
        """
        return _resolve_identity()
