from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
metrics = PrometheusMetrics()

def create_app():
    app = Flask(__name__)

    # Configuração: utilize variáveis de ambiente em produção
    app.config.from_object('app.config.Config')

    # Inicializa o banco de dados
    db.init_app(app)
    
    # Inicializa o Prometheus metrics
    metrics.init_app(app)

    # Importa e registra as rotas
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')
    
    # Registra o blueprint do ChatBot
    from app.chatbot import chatbot_bp
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    return app

