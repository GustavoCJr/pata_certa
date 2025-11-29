from flask import Blueprint, render_template, request, url_for, redirect, current_app, abort, flash
from forms import RegistrarPetForm, LoginForm
from models import Animal, Ong
from extensions import db, login_manager
from werkzeug.utils import secure_filename
import os
import uuid
from pathlib import Path
from sqlalchemy import select
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required

# 1. Cria o Blueprint (o agrupador de rotas)
main_bp = Blueprint('main', __name__) 


@main_bp.route('/')
def index():
    # Rotas do Blueprint usam main.index no url_for
    return render_template('index.html')


@main_bp.route('/sobre')
def sobre():
    return render_template('sobre.html')


@main_bp.route('/registrar_pet', methods=['GET', 'POST'])
@login_required
def registrar_pet():
    form = RegistrarPetForm()

    # verifica se é valido o formulario enviado
    if form.validate_on_submit():
        # 1. Lógica de Upload
        f = form.foto.data 
        original_filename = secure_filename(f.filename)
        file_ext = os.path.splitext(original_filename)[1]
        filename = str(uuid.uuid4()) + file_ext

        caminho_salvamento = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        imagem = Image.open(f)
        
        tamanho_maximo = (800, 800)
        
        imagem.thumbnail(tamanho_maximo) 
        
        imagem.save(caminho_salvamento, optimize=True, quality=75)
        
        foto_url = url_for('static', filename=f'uploads/{filename}') 
        
        # 2. Lógica de DB
        
        novo_animal = Animal(
            nome=form.nome.data, # type: ignore
            especie=form.especie.data, # type: ignore
            idade=form.idade.data, # type: ignore
            foto_url=foto_url, # type: ignore
            ong_id=current_user.id  # type: ignore
        )
        db.session.add(novo_animal)
        db.session.commit()
        
        # O url_for agora precisa do prefixo do Blueprint: 'main.exibir_pets'
        return redirect(url_for('main.exibir_pet', pet_id=novo_animal.id))

    # Para o método GET (renderiza o formulário) ou POST com erro
    return render_template('registrar_pet_form.html', form=form)


@main_bp.route('/exibir_pet/<int:pet_id>')
def exibir_pet(pet_id):
    # 1. Cria a consulta para buscar o Animal pelo ID
    # .scalar_one_or_none() é a forma elegante de buscar um único resultado
    stmt = select(Animal).filter_by(id=pet_id)
    pet = db.session.execute(stmt).scalar_one_or_none() 
    
    # 2. Verifica se o pet existe
    if pet is None:
        # Retorna um erro 404 (Não Encontrado) padrão do Flask
        abort(404, description="O pet solicitado não foi encontrado.")

    # 3. Passa o objeto 'pet' completo para o template
    return render_template('pet.html', pet=pet)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já estiver autenticado, redirecione para a home
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) 

    form = LoginForm()
    
    if form.validate_on_submit():
        # 1. Busca o usuário (ONG) pelo email
        stmt = select(Ong).filter_by(email=form.email.data)
        ong = db.session.execute(stmt).scalar_one_or_none()
        
        # 2. Verifica se a ONG existe E se a senha está correta
        if ong is None or not ong.check_password(form.password.data):
            flash('E-mail ou senha inválidos', 'danger')
            return redirect(url_for('main.login'))
        
        # 3. Login bem-sucedido
        login_user(ong, remember=form.remember_me.data)
        flash('Login realizado com sucesso!', 'success')
        
        # Redireciona para a próxima página (se houver, senão para a home)
        return redirect(url_for('main.index'))
        
    return render_template('login_form.html', form=form)


@main_bp.route('/logout')
@login_required # Garante que só usuários logados possam deslogar
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))