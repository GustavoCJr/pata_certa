# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired 


class RegistrarPetForm(FlaskForm):
    nome = StringField('Nome do Animal', [validators.DataRequired(), validators.Length(min=2, max=50)])
    especie = StringField('Espécie', [validators.DataRequired()])
    idade = IntegerField('Idade', [validators.Optional(), validators.NumberRange(min=0, max=30)])
    
    foto = FileField('Foto do Animal', validators=[
        FileRequired(message='É obrigatório enviar uma foto.'), # Garante que o arquivo foi enviado
        FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens JPG, PNG ou JPEG são permitidas.') # Restringe os tipos de arquivo
    ])

    
    submit = SubmitField('Registrar Pet')