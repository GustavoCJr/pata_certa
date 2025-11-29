import os
from pathlib import Path

# Determina o diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent

class Config:
    # ⚠️ MUITO IMPORTANTE: Defina esta chave em variáveis de ambiente na produção
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-super-chave-secreta-padrao-aqui' 

    DATABASE_PATH = BASE_DIR / 'instance' / 'patacerta.db'
    
    # Converte o caminho do Pathlib para string, prefixado com 'sqlite:///'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de Upload de Arquivos
    UPLOAD_FOLDER = str(BASE_DIR / 'static' / 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Exemplo: Limite de 16MB