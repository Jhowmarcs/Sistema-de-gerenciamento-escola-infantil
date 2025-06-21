from flask import Blueprint, request, jsonify
from app.models import Professor
from app import db

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    return jsonify([{
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    } for professor in professores])

@professores_bp.route('/', methods=['POST'])
def create_professor():
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
    professor = Professor.query.get_or_404(id_professor)
    return jsonify({
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    })

@professores_bp.route('/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
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
    professor = Professor.query.get_or_404(id_professor)
    
    try:
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'message': 'Professor excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir professor'}), 500