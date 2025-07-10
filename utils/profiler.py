from utils import Middleware
from flask import g, request
import time
import json
import os
from datetime import datetime


class Profiler:
    LOG_FILE = "logs/profiler_log.json"

    def __init__(self):
        self._ensure_log_directory()

    @staticmethod
    def _ensure_log_directory():
        """Ensure the logs folder exists"""
        log_dir = os.path.dirname(Profiler.LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    @staticmethod
    def get_tenant_key():
        auth_header = request.headers.get("Authorization", "")
        try:
            token = auth_header.split(" ")[1]
            decode = Middleware.decode_auth_token(token)
            current_user = decode["user"]
            return {
                "tenant_id": current_user.get("tenant_id", "anonymous"),
                "user_id": current_user.get("id", "anonymous"),
            }
        except:
            return {
                "tenant_id": "anonymous",
                "user_id": "anonymous"
            }

    @staticmethod
    def save_log_json(tenant_id, user_id, log_data):
        tenant_key = f"tenant_id_{tenant_id}"
        user_key = f"user_id_{user_id}"

        # Pastikan folder log ada
        log_dir = os.path.dirname(Profiler.LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Baca log yang ada
        if os.path.exists(Profiler.LOG_FILE):
            with open(Profiler.LOG_FILE, "r") as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = {}
        else:
            logs = {}

        # Buat struktur tenant dan user jika belum ada
        if tenant_key not in logs:
            logs[tenant_key] = {}

        if user_key not in logs[tenant_key]:
            logs[tenant_key][user_key] = []

        logs[tenant_key][user_key].append(log_data)

        # Simpan ulang
        with open(Profiler.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)

    @staticmethod
    def register_profiler(app):
        @app.before_request
        def start_timer():
            g.start_time = time.time()

        @app.after_request
        def log_request_time(response):
            if hasattr(g, 'start_time'):
                duration = time.time() - g.start_time
                endpoint = request.endpoint
                method = request.method
                path = request.path
                status = response.status_code

                key_data = Profiler.get_tenant_key()
                user_id = key_data.get("user_id")
                tenant_id = key_data.get("tenant_id")

                log_record = {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3],  # Format seperti log konvensional
                    "user_id": user_id,
                    "method": method,
                    "path": path,
                    "status": status,
                    "duration": round(duration, 4),
                    "endpoint": endpoint
                }

                Profiler.save_log_json(tenant_id, user_id, log_record)

                app.logger.info(
                    f"[Profiler] user_id={user_id} | {method} {path} -> {endpoint} | Took: {duration:.4f} sec"
                )

            return response
