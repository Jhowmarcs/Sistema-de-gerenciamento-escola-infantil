import os

class Config:
    # Exemplo de URL para o banco PostgreSQL:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://usuario:senha@db:5432/nome_banco'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
