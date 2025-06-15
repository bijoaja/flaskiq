import logging
import json
import os
from datetime import datetime
from flask_limiter import Limiter as FlaskLimiter
from flask import request
from utils.profiler import Profiler


class TenantRateLimiter:
    class SafeFormatter(logging.Formatter):
        def format(self, record):
            record.tenant = getattr(record, "tenant", "-")
            record.user_id = getattr(record, "user_id", "-")
            record.endpoint = getattr(record, "endpoint", "-")
            record.method = getattr(record, "method", "-")
            record.status = getattr(record, "status", "-")
            return super().format(record)

    def __init__(
        self, key_func=Profiler.get_tenant_key, default_limits=["100 per minutes"]
    ):
        self.key_func = key_func
        self.default_limits = default_limits
        self.limiter = FlaskLimiter(
            key_func=self.key_func, default_limits=self.default_limits
        )
        self.json_log_path = "logs/rate_limit.json"
        self._ensure_log_directory()
        self.logger = self._setup_logging()

    def init_app(self, app):
        self.limiter.init_app(app)
        self._register_signals()
        self._register_after_request(app)

    def limit(self, *args, **kwargs):
        return self.limiter.limit(*args, **kwargs)

    def _setup_logging(self):
        logger = logging.getLogger("limiter")
        logger.setLevel(logging.INFO)

        formatter = self.SafeFormatter(
            "[%(asctime)s] INFO in limiter: [RateLimiter] tenant=%(tenant)s | user_id=%(user_id)s | %(method)s %(endpoint)s | Status: %(status)s"
        )

        # Console log handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        logger.propagate = False
        return logger

    def _log_rate_limit(self, tenant, user_id, endpoint, method, status):
        # Logging to terminal and file
        self.logger.info(
            "Rate limit log",
            extra={
                "tenant": tenant or "-",
                "user_id": user_id or "-",
                "endpoint": endpoint or "-",
                "method": method or "-",
                "status": status or "-",
            },
        )

        # Logging to JSON
        self._log_to_json(tenant, user_id, method, endpoint, status)
        
    def _ensure_log_directory(self):
        """Ensure the logs directory exists"""
        log_dir = os.path.dirname(self.json_log_path)
        if not os.path.exists(log_dir):
            print(log_dir)
            os.makedirs(log_dir)

    def _log_to_json(self, tenant, user_id, method, endpoint, status):
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "method": method,
            "endpoint": endpoint,
            "status": status,
        }

        # Load existing log
        data = {}
        if os.path.exists(self.json_log_path):
            with open(self.json_log_path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        # Update log
        tenant=f"tenant_id_{tenant}"
        user_id=f"user_id_{user_id}"
        if tenant not in data:
            data[tenant] = {}

        if str(user_id) not in data[tenant]:
            data[tenant][str(user_id)] = []

        data[tenant][str(user_id)].append(log_entry)

        # Save log
        with open(self.json_log_path, "w") as f:
            json.dump(data, f, indent=2)

    def _register_after_request(self, app):
        @app.after_request
        def log_successful_request(response):
            if response.status_code != 429:
                tenant = self.key_func().get("tenant_id")
                user_id = self.key_func().get("user_id")
                self._log_rate_limit(
                    tenant, user_id, request.endpoint, request.method, "ALLOWED"
                )
            return response

    def _register_signals(self):
        try:
            from flask_limiter.signals import request_limit_exceeded

            @request_limit_exceeded.connect_via(self.limiter)
            def log_limit_exceeded(sender, request, **extra):
                tenant = self.key_func()
                user_id = getattr(request, "user_id", "-")
                self._log_rate_limit(
                    tenant, user_id, request.endpoint, request.method, "LIMIT EXCEEDED"
                )

        except ImportError:
            pass  # Versi Flask-Limiter tidak mendukung signals
