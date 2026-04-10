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

import time
import logging
from functools import wraps
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
            import jwt
            import os
            token = auth_header.split(" ", 1)[1]
            payload = jwt.decode(
                token, os.getenv("JWT_KEY", ""), algorithms=["HS256"]
            )
            user_id = payload.get("user", {}).get("id")
            if user_id:
                return f"user:{user_id}"
        except Exception:
            pass
    return f"ip:{request.remote_addr}"


class Profiler:

    @staticmethod
    def register_profiler(app) -> None:
        """Register before/after hooks to log every request duration."""

        @app.before_request
        def _start_timer():
            g.start_time = time.perf_counter()

        @app.after_request
        def _log_request(response):
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
    def track(func):
        """Decorator — logs execution time of any function.

        Works inside and outside a request context.

        Example::

            @Profiler.track
            def send_email(to):
                ...
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
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
