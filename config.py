import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the entire system"""
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Keys and security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    WTF_CSRF_SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # JWT
    JWT_KEY = os.getenv('JWT_KEY', 'your-jwt-secret-here')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRY_MINUTES = int(os.getenv('JWT_EXPIRY_MINUTES', '60'))

    # AI / LLM
    AI_KEY = os.environ.get("AI_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "ollama")   # "ollama" | "openai"
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///flaskiq.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Docs using swagger
    SWAGGER = {'swaggerui': True}
    DEBUG = True

    # CORS configuration
    CORS_ORIGINS = ['*']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}