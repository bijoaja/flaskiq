import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the entire system"""
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # KEY for AI and SECRET Key
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    AI_KEY = os.environ.get("AI_KEY")
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST")

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