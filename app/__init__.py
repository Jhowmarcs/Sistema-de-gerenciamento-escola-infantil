from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
from flasgger import Swagger
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/escola_infantil')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensões
    db.init_app(app)
    CORS(app)
    Swagger(app)  # Garante que o Swagger está registrado
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.alunos import alunos_bp
    from app.routes.professores import professores_bp
    from app.routes.turmas import turmas_bp
    from app.routes.pagamentos import pagamentos_bp
    from app.routes.presencas import presencas_bp
    from app.routes.atividades import atividades_bp
    from app.routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(alunos_bp, url_prefix='/api/alunos')
    app.register_blueprint(professores_bp, url_prefix='/api/professores')
    app.register_blueprint(turmas_bp, url_prefix='/api/turmas')
    app.register_blueprint(pagamentos_bp, url_prefix='/api/pagamentos')
    app.register_blueprint(presencas_bp, url_prefix='/api/presencas')
    app.register_blueprint(atividades_bp, url_prefix='/api/atividades')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    # Rota inicial
    @app.route("/")
    def index():
        return "API do Sistema Escolar Infantil está rodando!"

    # Inicializar PrometheusMetrics após os blueprints
    PrometheusMetrics(app)
    print('URL MAP:', app.url_map)  # Debug: mostra todos os endpoints registrados

    return app