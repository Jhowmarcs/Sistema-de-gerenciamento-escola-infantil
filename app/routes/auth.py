from flask import Blueprint, request, jsonify
from app.models import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Realizar login de usuário
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - login
            - senha
          properties:
            login:
              type: string
              example: "admin"
            senha:
              type: string
              example: "123456"
    responses:
      200:
        description: Login realizado com sucesso
        examples:
          application/json: {
            "message": "Login realizado com sucesso",
            "usuario": {
              "id": 1,
              "login": "admin",
              "nivel_acesso": "admin",
              "id_professor": null
            }
          }
      400:
        description: Login e senha obrigatórios
        examples:
          application/json: {"error": "Login e senha são obrigatórios"}
      401:
        description: Credenciais inválidas
        examples:
          application/json: {"error": "Credenciais inválidas"}
    """
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
    """
    Registrar novo usuário
    ---
    tags:
      - Autenticação
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - login
            - senha
            - nivel_acesso
          properties:
            login:
              type: string
              example: "professor1"
            senha:
              type: string
              example: "senha123"
            nivel_acesso:
              type: string
              example: "professor"
            id_professor:
              type: integer
              example: 2
    responses:
      201:
        description: Usuário criado com sucesso
        examples:
          application/json: {"message": "Usuário criado com sucesso"}
      400:
        description: Dados incompletos
        examples:
          application/json: {"error": "Dados incompletos"}
      409:
        description: Login já existe
        examples:
          application/json: {"error": "Login já existe"}
      500:
        description: Erro ao criar usuário
        examples:
          application/json: {"error": "Erro ao criar usuário"}
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ('login', 'senha', 'nivel_acesso')):
        return jsonify({'error': 'Dados incompletos'}), 400

    # Mapeamento para aceitar valores do frontend
    mapa_nivel_acesso = {
        'administrador': 'administrador',
        'admin': 'administrador',
        'secretaria': 'secretaria',
        'professor': 'professor'
    }
    nivel = data['nivel_acesso'].strip().lower()
    nivel_convertido = mapa_nivel_acesso.get(nivel)
    if not nivel_convertido:
        return jsonify({'error': f"Valor de nivel_acesso inválido. Use um destes: {list(mapa_nivel_acesso.keys())}"}), 400

    if Usuario.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Login já existe'}), 409
    
    usuario = Usuario(
        login=data['login'],
        senha=data['senha'],  # Em produção, usar hash
        nivel_acesso=nivel_convertido,
        id_professor=data.get('id_professor')
    )
    
    try:
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar usuário'}), 500