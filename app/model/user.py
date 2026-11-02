from datetime import datetime
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model):
    __tablename__ = "users"

    id: Any = db.Column(db.Integer, primary_key=True)
    username: Any = db.Column(db.String(100), unique=True, nullable=False)
    email: Any = db.Column(db.String(150), unique=True, nullable=False)
    password_hash: Any = db.Column(db.String(200), nullable=False)
    created_at: Any = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(str(self.password_hash), password)
