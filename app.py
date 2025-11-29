from flask import Flask
import os
from extensions import db 
from config import Config
from views.main import main_bp

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
    app = create_app()
    
    with app.app_context():
        from models import Animal, Ong, Usuario, PedidoAdocao
        db.create_all()
    
    app.run(debug=True)