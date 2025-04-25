from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração: utilize variáveis de ambiente em produção
    app.config.from_object('app.config.Config')

    # Inicializa o banco de dados
    db.init_app(app)

    # Importa e registra as rotas
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')

    return app

