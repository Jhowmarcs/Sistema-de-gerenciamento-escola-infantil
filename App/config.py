import os
from datetime import timedelta

class Config:
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:secret@db:5432/nome_banco')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-desenvolvimento')
    
    # Configuração de logs
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configuração de timeout da sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    
    # Configuração do servidor
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
