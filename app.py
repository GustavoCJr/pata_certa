from flask import Flask, render_template, request, url_for, redirect
import os
from werkzeug.utils import secure_filename

from forms import RegistrarPetForm
from db.model_db import Animal, Ong, Usuario, PedidoAdocao

app = Flask(__name__)

# PASTA DE UPLOAD
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
# ================================================================



@app.route('/')
def index():
    return render_template('index.html')




@app.route('/sobre')
def sobre():
    return render_template('sobre.html')




@app.route('/registrar_pet', methods=['POST'])
def registrar_pet():
    form = RegistrarPetForm()

    if form.validate_on_submit():
        # 1. Obtém o objeto FileStorage do WTForms
        f = form.foto.data 
        
        # 2. Gera um nome de arquivo seguro (remove espaços, caracteres especiais)
        filename = secure_filename(f.filename)
        
        # 3. Define o caminho completo para salvar o arquivo
        caminho_salvamento = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 4. Salva o arquivo no disco
        f.save(caminho_salvamento)
        
        # 5. Salva o caminho do arquivo no banco de dados
        # O URL público para acessar a imagem será: /static/uploads/nome_do_arquivo.jpg
        foto_url = url_for('static', filename=f'uploads/{filename}') 
        
        # --- Lógica de Salvamento no DB (SQLAlchemy) ---
        novo_animal = Animal(
            nome=form.nome.data,
            especie=form.especie.data,
            idade=form.idade.data,
            foto_url=foto_url, # Salva o URL para exibição
            ong_id=current_user.id #(Adicione a ONG logada aqui)
        )
        db.session.add(novo_animal)
        db.session.commit()
        
        return redirect(url_for('exibir_pets'))

    return render_template('registrar_pet_form.html', form=form)




@app.route('/exibir_pets')
def exibir_pets():
    return render_template('pet.html')
