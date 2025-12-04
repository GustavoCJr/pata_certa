from flask import Flask
import os
from extensions import db
from flask_login import LoginManager
from config import Config
from views.main import main_bp
from views.api_routes import api_bp
from seed import seed_data
from models import Ong

"""
def cleanup_development_environment():
    '''Remove o DB e o conteúdo dos uploads para um estado limpo de desenvolvimento.'''
    db_path = Config.DATABASE_PATH
    upload_dir = Config.UPLOAD_FOLDER
    instance_dir = Config.BASE_DIR / 'instance'  # O caminho da pasta instance

    # 1. Remove o arquivo DB se ele existir
    if os.path.exists(db_path):
        os.remove(db_path)

    # 2. Remove a pasta de uploads se ela existir
    if os.path.exists(upload_dir):
        # Remove a pasta e todo o seu conteúdo
        shutil.rmtree(upload_dir) 

    # 3. CRIAÇÃO GARANTIDA DE DIRETÓRIOS (O FIX)
    # Garante que a pasta instance exista
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    # Garante que a pasta static/uploads exista
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
"""


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializa banco
    db.init_app(app)

    # Inicializa LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Ong, int(user_id))

    # Garante que pastas existam (mesmo usando PostgreSQL no Render)
    upload_path = app.config.get("UPLOAD_FOLDER")
    if upload_path and not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)

    # Registra rotas
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # Cria tabelas apenas localmente, não em produção
    if app.config.get("ENV") == "development":
        with app.app_context():
            db.create_all()
            seed_data(app)

    return app


# Instância usada pelo Gunicorn no Render
app = create_app()


if __name__ == "__main__":
    # Modo debug local
    with app.app_context():
        db.create_all()
        seed_data(app)

    app.run(debug=True)