"""
TenantRateLimiter — per-user rate limiting.

Authenticated requests are keyed by user ID from the JWT token.
Anonymous requests fall back to the client IP address.

App-wide default (100 req/min):
    rate_limiter = TenantRateLimiter()
    rate_limiter.init_app(app)

Per-route override:
    @rate_limiter.limit("10 per minute")
    def sensitive_endpoint():
        ...

Exempt a route entirely:
    @rate_limiter.exempt
    def health_check():
        ...
"""

import logging
from flask_limiter import Limiter as FlaskLimiter
from flask_limiter.util import get_remote_address
from flask import request

logger = logging.getLogger("flaskiq.limiter")


def _get_rate_limit_key() -> str:
    """Key function for Flask-Limiter.

    Authenticated → "user:<user_id>"   (same limit pool per user, any IP)
    Anonymous     → "ip:<remote_addr>" (limit pool per IP)

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
                key = f"user:{user_id}"
                logger.debug("Rate limit key: %s", key)
                return key
        except Exception:
            pass

    key = f"ip:{get_remote_address()}"
    logger.debug("Rate limit key: %s", key)
    return key


class TenantRateLimiter:

    def __init__(self, default_limits: list | None = None):
        self._default_limits = default_limits or ["100 per minute"]
        self._limiter = FlaskLimiter(
            key_func=_get_rate_limit_key,
            default_limits=self._default_limits,
        )

    def init_app(self, app) -> None:
        self._limiter.init_app(app)

    def limit(self, limit_value: str, **kwargs):
        """Apply a custom rate limit to a specific route.

        Example::

            @rate_limiter.limit("5 per minute")
            def login():
                ...
        """
        return self._limiter.limit(limit_value, **kwargs)

    def exempt(self, func):
        """Exempt a route from all rate limiting.

        Example::

            @rate_limiter.exempt
            def health():
                return "ok"
        """
        return self._limiter.exempt(func)
