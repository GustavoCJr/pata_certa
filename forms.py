# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators, PasswordField, BooleanField, ValidationError
from wtforms.validators import EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrarPetForm(FlaskForm):
    nome = StringField('Nome do Animal', [
                       validators.DataRequired(), validators.Length(min=2, max=50)])
    especie = StringField('Espécie', [validators.DataRequired()])
    idade = IntegerField(
        'Idade', [validators.Optional(), validators.NumberRange(min=0, max=30)])

    foto = FileField('Foto do Animal', validators=[
        # Garante que o arquivo foi enviado
        FileRequired(message='É obrigatório enviar uma foto.'),
        # Restringe os tipos de arquivo
        FileAllowed(['jpg', 'png', 'jpeg'],
                    'Apenas imagens JPG, PNG ou JPEG são permitidas.')
    ])

    submit = SubmitField('Registrar Pet')


class LoginForm(FlaskForm):
    email = StringField(
        'E-mail', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Senha', [validators.DataRequired()])
    remember_me = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')


class CadastroOngForm(FlaskForm):
    nome_fantasia = StringField('Nome Fantasia da ONG', [
                                validators.DataRequired(), validators.Length(min=3, max=100)])
    cnpj = StringField('CNPJ', [validators.DataRequired(), validators.Length(
        min=14, max=14, message="O CNPJ deve ter 14 dígitos.")])
    email = StringField(
        'E-mail', [validators.DataRequired(), validators.Email()])

    password = PasswordField('Senha', [
        validators.DataRequired(),
        validators.Length(
            min=6, message="A senha deve ter pelo menos 6 caracteres."),
        EqualTo('confirm', message='As senhas não coincidem.')
    ])
    confirm = PasswordField('Repita a Senha')

    submit = SubmitField('Cadastrar ONG')

    # VALIDADOR PERSONALIZADO: Garante que o CNPJ ou E-mail não estão duplicados
    def validate_cnpj(self, cnpj):
        from models import Ong
        from extensions import db
        if db.session.execute(db.select(Ong).filter_by(cnpj=cnpj.data)).scalar_one_or_none():
            raise ValidationError('CNPJ já cadastrado. Use outro.')

    def validate_email(self, email):
        from models import Ong
        from extensions import db
        if db.session.execute(db.select(Ong).filter_by(email=email.data)).scalar_one_or_none():
            raise ValidationError('E-mail já cadastrado. Use outro.')
