import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent
    # Configurações globais que valem para todos os ambientes (base)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-forte-e-padrao' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Caminhos estáticos (Usados tanto na inicialização do DB quanto na lógica de upload)
    DATABASE_DIR = BASE_DIR / 'instance'
    DATABASE_PATH = DATABASE_DIR / 'patacerta.db'
    UPLOAD_FOLDER = str(BASE_DIR / 'static' / 'uploads')


# Configuração para desenvolvimento (usando SQLite local)
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    # SQLite local (com o caminho absoluto)
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{Config.DATABASE_PATH}'


# Configuração para produção (usando PostgreSQL remoto)
class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    # PostgreSQL URI lida de uma variável de ambiente (PADRÃO DE DEPLOY)
    # A variável de ambiente DATABASE_URL deve ser setada no servidor
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')