import pytest
import json
from app import create_app, db
from app.models import Usuario, Professor, Turma, Aluno

@pytest.fixture
def app():
    """Criar aplicação de teste"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        
        # Criar dados de teste
        professor = Professor(
            nome_completo='Professor Teste',
            email='teste@teste.com',
            telefone='11999999999'
        )
        db.session.add(professor)
        db.session.flush()
        
        turma = Turma(
            nome_turma='Turma Teste',
            id_professor=professor.id_professor,
            horario='08:00 - 12:00'
        )
        db.session.add(turma)
        db.session.flush()
        
        usuario = Usuario(
            login='teste',
            senha='123456',
            nivel_acesso='administrador'
        )
        db.session.add(usuario)
        db.session.commit()
        
        yield app
        
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de teste"""
    return app.test_client()

def test_health_check(client):
    """Testar endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_login_success(client):
    """Testar login com sucesso"""
    response = client.post('/api/auth/login', 
                          json={'login': 'teste', 'senha': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'usuario' in data

def test_login_failure(client):
    """Testar login com falha"""
    response = client.post('/api/auth/login', 
                          json={'login': 'teste', 'senha': 'senha_errada'})
    assert response.status_code == 401

def test_get_professores(client):
    """Testar listagem de professores"""
    response = client.get('/api/professores')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_create_professor(client):
    """Testar criação de professor"""
    data = {
        'nome_completo': 'Novo Professor',
        'email': 'novo@teste.com',
        'telefone': '11888888888'
    }
    response = client.post('/api/professores', json=data)
    assert response.status_code == 201

def test_get_turmas(client):
    """Testar listagem de turmas"""
    response = client.get('/api/turmas')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) > 0

def test_chatbot_message(client):
    """Testar envio de mensagem para o chatbot"""
    data = {'mensagem': 'Olá'}
    response = client.post('/api/chatbot/mensagem', json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'resposta_bot' in data