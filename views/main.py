from flask import Blueprint, render_template, request, url_for, redirect, current_app, abort, flash, jsonify
from forms import RegistrarPetForm, LoginForm, CadastroOngForm
from models import Animal, Ong
from extensions import db, login_manager
from werkzeug.utils import secure_filename
import os
import uuid
from pathlib import Path
from sqlalchemy import select, desc
from PIL import Image
from flask_login import login_user, logout_user, current_user, login_required

# 1. Cria o Blueprint (o agrupador de rotas)
main_bp = Blueprint('main', __name__) 


@main_bp.route('/')
def index():
    # Rotas do Blueprint usam main.index no url_for
    pets = db.session.query(Animal).order_by(func.random()).limit(3).all()
    return render_template('index.html', pets=pets)


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

@main_bp.route('/api/logged')
def api_logged():
    """
    Retorna se o usuário está autenticado e um campo 'username' seguro
    (tenta 'username', depois 'name', depois 'email', senão None).
    """
    if not current_user.is_authenticated:
        return jsonify({"logged": False, "username": None})

    # tenta obter um nome de exibição de forma segura
    username = getattr(current_user, 'username', None)
    if not username:
        username = getattr(current_user, 'name', None)
    if not username:
        username = getattr(current_user, 'email', None)

    return jsonify({"logged": True, "username": username})

    
@main_bp.route('/logout')
@login_required # Garante que só usuários logados possam deslogar
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))


@main_bp.route('/cadastro/ong', methods=['GET', 'POST'])
def cadastro_ong():
    # Redireciona se o usuário já estiver logado
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = CadastroOngForm()
    
    if form.validate_on_submit():
        # 1. Cria o novo objeto ONG
        nova_ong = Ong(
            nome_fantasia=form.nome_fantasia.data, # type: ignore
            cnpj=form.cnpj.data, # type: ignore
            email=form.email.data, # type: ignore
        )
        
        nova_ong.set_password(form.password.data)
        
        db.session.add(nova_ong)
        db.session.commit()
        
        login_user(nova_ong) 

        flash('ONG cadastrada com sucesso! Você pode fazer login.', 'success')
        
        # Redireciona para a página de login
        return redirect(url_for('main.login'))

    # Se GET ou validação falhar, exibe o formulário
    return render_template('cadastro_ong_form.html', form=form)


# --- ROTAS API ---

@main_bp.route('/api/v1/pets', methods=['GET'])
def get_pets_paginated_json():
    
    # 1. Captura e Validação dos Parâmetros de Consulta
    try:
        # Parâmetros de Paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
    except ValueError:
        return jsonify({"error": "Parâmetros 'page', 'per_page' e 'ong_id' devem ser números inteiros válidos."}), 400

    if page < 1 or per_page < 1:
        return jsonify({"error": "Parâmetros devem ser maiores que zero."}), 400


    ong_ids_raw = request.args.getlist('ong_id') 

    # Converte os IDs de string para inteiro e remove valores vazios
    ong_ids_filter = [int(id) for id in ong_ids_raw if id.isdigit()]
    
    # 2. Constrói a consulta base e a consulta de contagem
    stmt = select(Animal)
    count_stmt = select(db.func.count()).select_from(Animal) 
    
    # 3. Adiciona o filtro condicional (Se houver IDs na lista)
    if ong_ids_filter:
        # Aplica o filtro usando o operador .in_()
        stmt = stmt.filter(Animal.ong_id.in_(ong_ids_filter))
        count_stmt = count_stmt.filter(Animal.ong_id.in_(ong_ids_filter))
        
    # 4. Calcula o offset e aplica ordenação e paginação
    offset = (page - 1) * per_page
    
    # Consulta paginada final
    stmt = stmt.order_by(desc(Animal.id)).offset(offset).limit(per_page)
    pets = db.session.execute(stmt).scalars().all()
    
    # 5. Cálculo dos Metadados
    total_pets = db.session.scalar(count_stmt) or 0
    total_pages = (total_pets + per_page - 1) // per_page 
    
    # ... (restante da serialização e retorno do JSON) ...
    pets_list = []
    for pet in pets:
        pets_list.append({
            'id': pet.id,
            'nome': pet.nome,
            'especie': pet.especie,
            'idade': pet.idade,
            'foto_url': pet.foto_url,
            'ong_id': pet.ong_id 
        })
        
    return jsonify({
        'data': pets_list,
        'pagination': {
            'total_items': total_pets,
            'total_pages': total_pages,
            'current_page': page,
            'items_per_page': per_page,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    })
@main_bp.route('/adocao')
def adocao():
    """Página de pets para adoção com paginação."""
    from math import ceil

    page = request.args.get('page', 1, type=int)
    PER_PAGE = 16

    # Conta total de pets
    total_pets = db.session.query(Animal).count()
    total_pages = ceil(total_pets / PER_PAGE) if total_pets else 1

    # Ajusta page caso inválido
    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    # Busca paginada
    pets = (db.session.query(Animal)
            .order_by(Animal.id.desc())
            .offset((page - 1) * PER_PAGE)
            .limit(PER_PAGE)
            .all())

    return render_template(
        "adocao.html",
        pets=pets,
        page=page,
        total_pages=total_pages
    )
from sqlalchemy import func

# exemplo dentro do blueprint main_bp
from sqlalchemy import func

@main_bp.route('/debug/random')
def debug_random():
    from sqlalchemy import func
    pets = db.session.query(Animal).order_by(func.random()).limit(3).all()
    return {
        "pets": [
            {
                "id": p.id,
                "nome": p.nome,
                "especie": p.especie,
                "idade": p.idade,
                "foto_url": p.foto_url
            }
            for p in pets
        ]
    }
# lista as ONGs com paginação simples
@main_bp.route('/ongs')
def ongs():
    """
    Lista as ONGs cadastradas.
    Querystring opcional: ?page=1
    """
    from math import ceil

    page = request.args.get('page', 1, type=int)
    PER_PAGE = 12  # ONGs por página

    total = db.session.query(Ong).count()
    total_pages = ceil(total / PER_PAGE) if total else 1

    if page < 1:
        page = 1
    if page > total_pages:
        page = total_pages

    ongs = (
        db.session.query(Ong)
        .order_by(Ong.id.desc())
        .offset((page - 1) * PER_PAGE)
        .limit(PER_PAGE)
        .all()
    )

    return render_template('ongs.html', ongs=ongs, page=page, total_pages=total_pages)
from flask import abort, render_template

@main_bp.route('/ong/<int:ong_id>')
def exibir_ong(ong_id):
    # busca a ONG pelo id
    ong = db.session.query(Ong).get(ong_id)  # ou use .filter_by(id=ong_id).first()
    if ong is None:
        abort(404)
    return render_template('exibir_ong.html', ong=ong)
