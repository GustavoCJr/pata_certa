import os
import sys
from app import create_app
from extensions import db
from seed import seed_data
# Importamos todos os modelos para que o db.create_all os reconheça
from models import * # Força o ambiente de produção para garantir que a URI do PostgreSQL seja usada
# O Render já deve ter setado FLASK_ENV=production ou equivalente
os.environ['FLASK_ENV'] = 'production' 

# Cria a instância da aplicação no contexto de Produção
app = create_app('production') 

# O bloco with app.app_context é necessário para operações de DB
with app.app_context():
    print("--- INICIANDO SETUP DE PRODUÇÃO NO POSTGRESQL ---")
    
    try:
        # 1. Criação de Tabelas
        # Se as tabelas já existirem (após o primeiro deploy), este comando é ignorado.
        db.create_all()
        print("✅ Tabelas do PostgreSQL criadas (ou verificadas) com sucesso.")

        # 2. Povoamento Inicial (Seeding)
        seed_data(app)
        print("✅ Dados iniciais (seed) inseridos com sucesso.")
        
    except Exception as e:
        print(f"❌ ERRO FATAL AO CONFIGURAR O BANCO DE DADOS: {e}")
        # É crucial encerrar o deploy se a conexão com o DB falhar
        sys.exit(1) 
        
    print("--- SETUP DE PRODUÇÃO FINALIZADO ---")