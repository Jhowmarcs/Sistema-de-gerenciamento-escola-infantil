from flask import Blueprint, request, jsonify
from app.models import Professor
from app import db

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def get_professores():
    """
    Listar todos os professores
    ---
    tags:
      - Professores
    responses:
      200:
        description: Lista de professores cadastrados
        examples:
          application/json: [
            {
              "id_professor": 1,
              "nome_completo": "Ana Paula Souza",
              "email": "ana.souza@escola.com",
              "telefone": "(11) 91234-5678"
            },
            {
              "id_professor": 2,
              "nome_completo": "Carlos Silva",
              "email": "carlos.silva@escola.com",
              "telefone": "(11) 99876-5432"
            }
          ]
    """
    professores = Professor.query.all()
    return jsonify([{
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    } for professor in professores])

@professores_bp.route('/', methods=['POST'])
def create_professor():
    """
    Cadastrar um novo professor
    ---
    tags:
      - Professores
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome_completo
            - email
            - telefone
          properties:
            nome_completo:
              type: string
              example: "Ana Paula Souza"
            email:
              type: string
              example: "ana.souza@escola.com"
            telefone:
              type: string
              example: "(11) 91234-5678"
    responses:
      201:
        description: Professor criado com sucesso
        examples:
          application/json: {"message": "Professor criado com sucesso", "id": 3}
      400:
        description: Dados incompletos
        examples:
          application/json: {"error": "Dados incompletos"}
      500:
        description: Erro ao criar professor
        examples:
          application/json: {"error": "Erro ao criar professor"}
    """
    data = request.get_json()
    
    required_fields = ['nome_completo', 'email', 'telefone']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        professor = Professor(
            nome_completo=data['nome_completo'],
            email=data['email'],
            telefone=data['telefone']
        )
        
        db.session.add(professor)
        db.session.commit()
        
        return jsonify({'message': 'Professor criado com sucesso', 'id': professor.id_professor}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar professor'}), 500

@professores_bp.route('/<int:id_professor>', methods=['GET'])
def get_professor(id_professor):
    """
    Buscar um professor pelo ID
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        type: integer
        required: true
        description: ID do professor
        example: 1
    responses:
      200:
        description: Dados do professor
        examples:
          application/json: {
            "id_professor": 1,
            "nome_completo": "Ana Paula Souza",
            "email": "ana.souza@escola.com",
            "telefone": "(11) 91234-5678"
          }
      404:
        description: Professor não encontrado
    """
    professor = Professor.query.get_or_404(id_professor)
    return jsonify({
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    })

@professores_bp.route('/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    """
    Atualizar dados de um professor
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        type: integer
        required: true
        description: ID do professor
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              example: "Ana Paula Souza"
            email:
              type: string
              example: "ana.souza@escola.com"
            telefone:
              type: string
              example: "(11) 91234-5678"
    responses:
      200:
        description: Professor atualizado com sucesso
        examples:
          application/json: {"message": "Professor atualizado com sucesso"}
      400:
        description: Dados não fornecidos
        examples:
          application/json: {"error": "Dados não fornecidos"}
      404:
        description: Professor não encontrado
      500:
        description: Erro ao atualizar professor
        examples:
          application/json: {"error": "Erro ao atualizar professor"}
    """
    professor = Professor.query.get_or_404(id_professor)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome_completo' in data:
            professor.nome_completo = data['nome_completo']
        if 'email' in data:
            professor.email = data['email']
        if 'telefone' in data:
            professor.telefone = data['telefone']
        
        db.session.commit()
        return jsonify({'message': 'Professor atualizado com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar professor'}), 500

@professores_bp.route('/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    """
    Excluir um professor
    ---
    tags:
      - Professores
    parameters:
      - name: id_professor
        in: path
        type: integer
        required: true
        description: ID do professor
        example: 1
    responses:
      200:
        description: Professor excluído com sucesso
        examples:
          application/json: {"message": "Professor excluído com sucesso"}
      404:
        description: Professor não encontrado
      500:
        description: Erro ao excluir professor
        examples:
          application/json: {"error": "Erro ao excluir professor"}
    """
    professor = Professor.query.get_or_404(id_professor)
    
    try:
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir professor'}), 500