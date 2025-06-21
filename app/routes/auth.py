from flask import Blueprint, request, jsonify
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('login') or not data.get('senha'):
        return jsonify({'error': 'Login e senha são obrigatórios'}), 400
    
    usuario = Usuario.query.filter_by(login=data['login']).first()
    
    if usuario and usuario.senha == data['senha']:  # Em produção, usar hash
        return jsonify({
            'message': 'Login realizado com sucesso',
            'usuario': {
                'id': usuario.id_usuario,
                'login': usuario.login,
                'nivel_acesso': usuario.nivel_acesso,
                'id_professor': usuario.id_professor
            }
        }), 200
    
    return jsonify({'error': 'Credenciais inválidas'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not all(k in data for k in ('login', 'senha', 'nivel_acesso')):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    if Usuario.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Login já existe'}), 409
    
    usuario = Usuario(
        login=data['login'],
        senha=data['senha'],  # Em produção, usar hash
        nivel_acesso=data['nivel_acesso'],
        id_professor=data.get('id_professor')
    )
    
    try:
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar usuário'}), 500