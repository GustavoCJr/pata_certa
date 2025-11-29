# seed.py

from extensions import db
from models import Ong, Animal
from werkzeug.security import generate_password_hash # Importa para garantir que o hashing esteja disponível

# Dados de teste para ONGs
ONG_DATA = [
    {
        'nome_fantasia': 'ONG PataCerta Teste',
        'cnpj': '11111111111111',
        'email': 'teste@ong1.org',
        'password': 'senha123', # Senha conhecida para teste de login
        'id_manual': 1 # Define ID para facilitar o relacionamento
    },
    {
        'nome_fantasia': 'ONG Amigos dos Bichos',
        'cnpj': '22222222222222',
        'email': 'contato@ong2.org',
        'password': 'senha123',
        'id_manual': 2
    },
    {
        'nome_fantasia': 'ONG Viva a Patinha',
        'cnpj': '33333333333333',
        'email': 'ajuda@ong3.org',
        'password': 'senha123',
        'id_manual': 3
    }
]

# Dados de teste para Pets (15 no total, para testar paginação)
PET_DATA = [
    # Pets da ONG 1
    {'nome': 'Toby', 'especie': 'Cachorro', 'idade': 3, 'ong_id': 1},
    {'nome': 'Luna', 'especie': 'Gato', 'idade': 1, 'ong_id': 1},
    {'nome': 'Max', 'especie': 'Cachorro', 'idade': 8, 'ong_id': 1},
    {'nome': 'Frajola', 'especie': 'Gato', 'idade': 5, 'ong_id': 1},
    
    # Pets da ONG 2
    {'nome': 'Rex', 'especie': 'Cachorro', 'idade': 2, 'ong_id': 2},
    {'nome': 'Miau', 'especie': 'Gato', 'idade': 10, 'ong_id': 2},
    {'nome': 'Cacau', 'especie': 'Cachorro', 'idade': 4, 'ong_id': 2},
    {'nome': 'Biscoito', 'especie': 'Outros', 'idade': 0, 'ong_id': 2},
    {'nome': 'Amora', 'especie': 'Gato', 'idade': 6, 'ong_id': 2},

    # Pets da ONG 3
    {'nome': 'Pingo', 'especie': 'Cachorro', 'idade': 7, 'ong_id': 3},
    {'nome': 'Nina', 'especie': 'Gato', 'idade': 3, 'ong_id': 3},
    {'nome': 'Mel', 'especie': 'Cachorro', 'idade': 9, 'ong_id': 3},
    {'nome': 'Pipoca', 'especie': 'Outros', 'idade': 1, 'ong_id': 3},
    {'nome': 'Kiwi', 'especie': 'Gato', 'idade': 2, 'ong_id': 3},
    {'nome': 'Pantera', 'especie': 'Cachorro', 'idade': 5, 'ong_id': 3},
]


def seed_data(app):
    """Cria dados iniciais para o ambiente de desenvolvimento."""
    
    with app.app_context():
        # Se as tabelas estiverem vazias, povoa o DB
        if db.session.query(Ong).count() == 0:
            print("\n--- INSERINDO DADOS DE TESTE (SEED) ---")
            
            # --- 1. CRIAÇÃO DAS ONGS ---
            for data in ONG_DATA:
                # Cria a ONG
                ong = Ong(
                    id=data['id_manual'], # Define o ID para garantir o FK
                    nome_fantasia=data['nome_fantasia'],
                    cnpj=data['cnpj'],
                    email=data['email'],
                )
                # Define a senha com hashing
                ong.set_password(data['password'])
                
                db.session.add(ong)
            
            db.session.commit()
            print(f"✅ {len(ONG_DATA)} ONGs criadas com sucesso.")

            # --- 2. CRIAÇÃO DOS PETS ---
            for i, data in enumerate(PET_DATA):
                # Usamos um URL de imagem simples para teste
                # Em um projeto real, você usaria url_for('static', filename=...)
                foto_url = f"/static/images/default/pet{i+1}.png"
                
                pet = Animal(
                    nome=data['nome'],
                    especie=data['especie'],
                    idade=data['idade'],
                    foto_url=foto_url,
                    ong_id=data['ong_id']
                )
                db.session.add(pet)
            
            db.session.commit()
            print(f"✅ {len(PET_DATA)} Pets criados e relacionados às ONGs.")
        else:
            print("✅ Dados de seed já existem (pulando criação).")