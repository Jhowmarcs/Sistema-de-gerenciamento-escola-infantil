from flask import Blueprint, request, jsonify
from app.models import Aluno
from app import db
from datetime import datetime

alunos_bp = Blueprint('alunos', __name__)

@alunos_bp.route('/', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    return jsonify([{
        'id_aluno': aluno.id_aluno,
        'nome_completo': aluno.nome_completo,
        'data_nascimento': aluno.data_nascimento.isoformat(),
        'id_turma': aluno.id_turma,
        'nome_responsavel': aluno.nome_responsavel,
        'telefone_responsavel': aluno.telefone_responsavel,
        'email_responsavel': aluno.email_responsavel,
        'informacoes_adicionais': aluno.informacoes_adicionais
    } for aluno in alunos])

@alunos_bp.route('/', methods=['POST'])
def create_aluno():
    data = request.get_json()
    
    required_fields = ['nome_completo', 'data_nascimento', 'id_turma', 
                      'nome_responsavel', 'telefone_responsavel', 'email_responsavel']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        
        aluno = Aluno(
            nome_completo=data['nome_completo'],
            data_nascimento=data_nascimento,
            id_turma=data['id_turma'],
            nome_responsavel=data['nome_responsavel'],
            telefone_responsavel=data['telefone_responsavel'],
            email_responsavel=data['email_responsavel'],
            informacoes_adicionais=data.get('informacoes_adicionais', '')
        )
        
        db.session.add(aluno)
        db.session.commit()
        
        return jsonify({'message': 'Aluno criado com sucesso', 'id': aluno.id_aluno}), 201
        
    except ValueError:
        return jsonify({'error': 'Data de nascimento inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar aluno'}), 500

@alunos_bp.route('/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno)
    return jsonify({
        'id_aluno': aluno.id_aluno,
        'nome_completo': aluno.nome_completo,
        'data_nascimento': aluno.data_nascimento.isoformat(),
        'id_turma': aluno.id_turma,
        'nome_responsavel': aluno.nome_responsavel,
        'telefone_responsavel': aluno.telefone_responsavel,
        'email_responsavel': aluno.email_responsavel,
        'informacoes_adicionais': aluno.informacoes_adicionais
    })

@alunos_bp.route('/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'nome_completo' in data:
            aluno.nome_completo = data['nome_completo']
        if 'data_nascimento' in data:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        if 'id_turma' in data:
            aluno.id_turma = data['id_turma']
        if 'nome_responsavel' in data:
            aluno.nome_responsavel = data['nome_responsavel']
        if 'telefone_responsavel' in data:
            aluno.telefone_responsavel = data['telefone_responsavel']
        if 'email_responsavel' in data:
            aluno.email_responsavel = data['email_responsavel']
        if 'informacoes_adicionais' in data:
            aluno.informacoes_adicionais = data['informacoes_adicionais']
        
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado com sucesso'})
        
    except ValueError:
        return jsonify({'error': 'Data de nascimento inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar aluno'}), 500

@alunos_bp.route('/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno)
    
    try:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir aluno'}), 500