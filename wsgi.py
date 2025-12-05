import os
from app import create_app

# Carrega o ambiente de produção (que usará o PostgreSQL)
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()