from flask import Flask
import os
from extensions import db 
from config import Config
import shutil
from views.main import main_bp
from pathlib import Path

def cleanup_development_environment():
    """Remove o DB e o conteúdo dos uploads para um estado limpo de desenvolvimento."""
    
    db_path = Config.DATABASE_PATH
    upload_dir = Config.UPLOAD_FOLDER
    instance_dir = Config.BASE_DIR / 'instance'  # O caminho da pasta instance

    # 1. Remove o arquivo DB se ele existir
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"🧹 Banco de dados removido: {db_path}")

    # 2. Remove a pasta de uploads se ela existir
    if os.path.exists(upload_dir):
        # Remove a pasta e todo o seu conteúdo
        shutil.rmtree(upload_dir) 
        print(f"🧹 Pasta de uploads removida: {upload_dir}")

    # 3. CRIAÇÃO GARANTIDA DE DIRETÓRIOS (O FIX)
    # Garante que a pasta instance exista
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    # Garante que a pasta static/uploads exista
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    print(f"✅ Diretórios '{instance_dir}' e '{upload_dir}' garantidos.")

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    db.init_app(app)

    instance_path = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    upload_path = app.config['UPLOAD_FOLDER']

    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    app.register_blueprint(main_bp) 

    return app

if __name__ == '__main__':
    print("--- INICIANDO LIMPEZA DO AMBIENTE DEV ---")
    cleanup_development_environment()
    print("------------------------------------------")

    app = create_app()
    
    with app.app_context():
        from models import Animal, Ong, Usuario, PedidoAdocao
        db.create_all()
    
    app.run(debug=True)