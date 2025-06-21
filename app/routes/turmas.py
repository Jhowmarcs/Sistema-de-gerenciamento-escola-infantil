from flask import Blueprint, request, jsonify
from app.models import Turma
from app import db

turmas_bp = Blueprint('turmas', __name__)

@turmas_bp.route('/', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    return jsonify([{
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    } for turma in turmas])

@turmas_bp.route('/', methods=['POST'])
def create_turma():
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
    turma = Turma.query.get_or_404(id_turma)
    return jsonify({
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    })

@turmas_bp.route('/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
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
    turma = Turma.query.get_or_404(id_turma)
    
    try:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir turma'}), 500