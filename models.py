from datetime import datetime
from extensions import db

# imports de login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# --- Definição das Tabelas (Classes) ---
class Ong(db.Model, UserMixin):
    __tablename__ = 'ongs'
    id = db.Column(db.Integer, primary_key=True)
    nome_fantasia = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255))

    # Relacionamento com Animal
    animais = db.relationship('Animal', backref='ong_proprietaria', lazy=True)

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255))

    def set_password(self, password):
        self.senha_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha_hash, password)


class Animal(db.Model):
    __tablename__ = 'animais'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(20), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    foto_url = db.Column(db.String(80), nullable=False)
    ong_id = db.Column(db.Integer, db.ForeignKey('ongs.id'), nullable=False)


class PedidoAdocao(db.Model):
    __tablename__ = 'pedidos_adocao'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey(
        'animais.id'), nullable=False)
