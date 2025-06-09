import pytest
from app import create_app, db
from app.models import Aluno, Turma, Professor, Usuario

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    response = client.get('/api/')
    assert response.status_code == 200
    assert b'API do Sistema de Gerenciamento Escolar Infantil funcionando!' in response.data

def test_chatbot(client):
    response = client.post('/api/chatbot/', json={'message': 'Qual o horário da escola?'})
    assert response.status_code == 200
    assert 'horario' in response.json['response'].lower()