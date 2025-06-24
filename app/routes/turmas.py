from flask import Blueprint, request, jsonify
from app.models import Turma
from app import db

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/', methods=['GET'])
def get_turmas():
    """
    Listar todas as turmas
    ---
    tags:
      - Turmas
    responses:
      200:
        description: Lista de turmas cadastradas
        examples:
          application/json: [
            {
              "id_turma": 1,
              "nome_turma": "Maternal A",
              "id_professor": 1,
              "horario": "Segunda a Sexta, 08:00-12:00"
            },
            {
              "id_turma": 2,
              "nome_turma": "Pré II B",
              "id_professor": 2,
              "horario": "Segunda a Sexta, 13:00-17:00"
            }
          ]
    """
    turmas = Turma.query.all()
    return jsonify([{
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    } for turma in turmas])

@turmas_bp.route('/', methods=['POST'])
def create_turma():
    """
    Cadastrar uma nova turma
    ---
    tags:
      - Turmas
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - nome_turma
            - id_professor
            - horario
          properties:
            nome_turma:
              type: string
              example: "Maternal A"
            id_professor:
              type: integer
              example: 1
            horario:
              type: string
              example: "Segunda a Sexta, 08:00-12:00"
    responses:
      201:
        description: Turma criada com sucesso
        examples:
          application/json: {"message": "Turma criada com sucesso", "id": 3}
      400:
        description: Dados incompletos
        examples:
          application/json: {"error": "Dados incompletos"}
      500:
        description: Erro ao criar turma
        examples:
          application/json: {"error": "Erro ao criar turma"}
    """
    data = request.get_json()
    
    required_fields = ['nome_turma', 'id_professor', 'horario']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        turma = Turma(
            nome_turma=data['nome_turma'],
            id_professor=data['id_professor'],
            horario=data['horario']
        )
        
        db.session.add(turma)
        db.session.commit()
        
        return jsonify({'message': 'Turma criada com sucesso', 'id': turma.id_turma}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar turma'}), 500

@turmas_bp.route('/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    """
    Buscar uma turma pelo ID
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        type: integer
        required: true
        description: ID da turma
        example: 1
    responses:
      200:
        description: Dados da turma
        examples:
          application/json: {
            "id_turma": 1,
            "nome_turma": "Maternal A",
            "id_professor": 1,
            "horario": "Segunda a Sexta, 08:00-12:00"
          }
      404:
        description: Turma não encontrada
    """
    turma = Turma.query.get_or_404(id_turma)
    return jsonify({
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    })

@turmas_bp.route('/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    """
    Atualizar dados de uma turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        type: integer
        required: true
        description: ID da turma
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome_turma:
              type: string
              example: "Maternal A"
            id_professor:
              type: integer
              example: 1
            horario:
              type: string
              example: "Segunda a Sexta, 08:00-12:00"
    responses:
      200:
        description: Turma atualizada com sucesso
        examples:
          application/json: {"message": "Turma atualizada com sucesso"}
      400:
        description: Dados não fornecidos
        examples:
          application/json: {"error": "Dados não fornecidos"}
      404:
        description: Turma não encontrada
      500:
        description: Erro ao atualizar turma
        examples:
          application/json: {"error": "Erro ao atualizar turma"}
    """
    turma = Turma.query.get_or_404(id_turma)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome_turma' in data:
            turma.nome_turma = data['nome_turma']
        if 'id_professor' in data:
            turma.id_professor = data['id_professor']
        if 'horario' in data:
            turma.horario = data['horario']
        
        db.session.commit()
        return jsonify({'message': 'Turma atualizada com sucesso'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar turma'}), 500

@turmas_bp.route('/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    """
    Excluir uma turma
    ---
    tags:
      - Turmas
    parameters:
      - name: id_turma
        in: path
        type: integer
        required: true
        description: ID da turma
        example: 1
    responses:
      200:
        description: Turma excluída com sucesso
        examples:
          application/json: {"message": "Turma excluída com sucesso"}
      404:
        description: Turma não encontrada
      500:
        description: Erro ao excluir turma
        examples:
          application/json: {"error": "Erro ao excluir turma"}
    """
    turma = Turma.query.get_or_404(id_turma)
    
    try:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir turma'}), 500