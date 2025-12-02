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


api_bp = Blueprint('api', __name__)


@api_bp.route('/api/logged')
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


@api_bp.route('/debug/random')
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



@api_bp.route('/api/v1/pets', methods=['GET'])
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