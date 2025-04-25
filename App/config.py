import os

class Config:
    # Exemplo de URL para o banco PostgreSQL:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
