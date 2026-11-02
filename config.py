import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

MIN_SECRET_KEY_LENGTH = 32
INSECURE_SECRET_KEYS = {
    "your-secret-key-here",
    "change-me-in-production",
    "dev-secret",
    "ci-secret",
}


def validate_secret_key(key: str | None, min_length: int = MIN_SECRET_KEY_LENGTH) -> str:
    """Validate secret key meets minimum security criteria.

    Raises ValueError if key is missing, too short, or uses a known placeholder.
    """
    if not key:
        raise ValueError(f"SECRET_KEY must be at least {min_length} characters long (got 0).")
    if key in INSECURE_SECRET_KEYS or any(
        placeholder in key.lower()
        for placeholder in ("your-secret-key-here", "change-me-in-production", "dev-secret")
    ):
        raise ValueError(
            f"Insecure placeholder SECRET_KEY '{key}' detected. Set a random secret key."
        )
    if len(key) < min_length:
        raise ValueError(
            f"SECRET_KEY must be at least {min_length} characters long (got {len(key)})."
        )
    return key


class Config:
    """Configuration class for the entire system"""

    # Base directory
    BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))

    # Keys and security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    WTF_CSRF_SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

    # JWT
    JWT_KEY: str = os.getenv("JWT_KEY", "your-jwt-secret-here")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = int(os.getenv("JWT_EXPIRY_MINUTES", "60"))

    # AI / LLM
    AI_KEY: str = os.environ.get("AI_KEY", "")
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "ollama")  # "ollama" | "openai"
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OLLAMA_HOST: str = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")

    # Upload configuration
    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, "static", "uploads")

    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL", "sqlite:///flaskiq.db")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # API Docs using swagger
    SWAGGER: dict[str, Any] = {"swaggerui": True}
    DEBUG: bool = True

    # CORS configuration
    CORS_ORIGINS: list[str] = ["*"]


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG: bool = True
    TESTING: bool = False


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG: bool = False
    TESTING: bool = False

    @classmethod
    def validate(cls) -> None:
        """Validate production configuration parameters."""
        validate_secret_key(cls.SECRET_KEY)
        validate_secret_key(cls.JWT_KEY)


class TestingConfig(Config):
    """Testing configuration"""

    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"


config: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
