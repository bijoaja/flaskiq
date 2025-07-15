import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # KEY UNTUK AI dan SECRET Key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    AI_KEY = os.environ.get("AI_KEY")
    OLLAMA_HOST = os.environ.get("OLLAMA_HOST")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Untuk membuat dokumentasi terhadap API
    SWAGGER = {'swaggerui': True}
    DEBUG = True