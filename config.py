import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent

    SECRET_KEY = os.environ.get('SECRET_KEY', "dev-secret") or 'sua-chave-secreta'

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")   # <-- AQUI!
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(BASE_DIR / 'static' / 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
