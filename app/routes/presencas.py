from flask import Blueprint, request, jsonify
from app.models import Presenca, Aluno
from app import db
from datetime import datetime
from sqlalchemy import and_, func

presencas_bp = Blueprint('presencas', __name__)

@presencas_bp.route('/', methods=['GET'])
def get_presencas():
    presencas = Presenca.query.all()
    return jsonify([{
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': presenca.data_presenca.isoformat(),
        'presente': presenca.presente
    } for presenca in presencas])

@presencas_bp.route('/', methods=['POST'])
def create_presenca():
    data = request.get_json()
    
    required_fields = ['id_aluno', 'data_presenca', 'presente']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        data_presenca = datetime.strptime(data['data_presenca'], '%Y-%m-%d').date()
        
        # Verificar se já existe presença para este aluno nesta data
        presenca_existente = Presenca.query.filter_by(
            id_aluno=data['id_aluno'],
            data_presenca=data_presenca
        ).first()
        
        if presenca_existente:
            return jsonify({'error': 'Presença já registrada para este aluno nesta data'}), 409
        
        presenca = Presenca(
            id_aluno=data['id_aluno'],
            data_presenca=data_presenca,
            presente=data['presente']
        )
        
        db.session.add(presenca)
        db.session.commit()
        
        return jsonify({'message': 'Presença registrada com sucesso', 'id': presenca.id_presenca}), 201
        
    except ValueError:
        return jsonify({'error': 'Data de presença inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao registrar presença'}), 500

@presencas_bp.route('/data/<string:data>', methods=['GET'])
def get_presencas_data(data):
    try:
        data_presenca = datetime.strptime(data, '%Y-%m-%d').date()
        presencas = Presenca.query.filter_by(data_presenca=data_presenca).all()
        
        return jsonify([{
            'id_presenca': presenca.id_presenca,
            'id_aluno': presenca.id_aluno,
            'presente': presenca.presente,
            'aluno_nome': presenca.aluno.nome_completo if presenca.aluno else None
        } for presenca in presencas])
        
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400

@presencas_bp.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_presencas_aluno(id_aluno):
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Presenca.query.filter_by(id_aluno=id_aluno)
    
    if data_inicio and data_fim:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(
                and_(Presenca.data_presenca >= data_inicio,
                     Presenca.data_presenca <= data_fim)
            )
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
    
    presencas = query.all()
    
    total_dias = len(presencas)
    dias_presentes = sum(1 for p in presencas if p.presente)
    percentual_frequencia = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
    
    return jsonify({
        'id_aluno': id_aluno,
        'total_dias': total_dias,
        'dias_presentes': dias_presentes,
        'dias_ausentes': total_dias - dias_presentes,
        'percentual_frequencia': round(percentual_frequencia, 2),
        'presencas': [{
            'id_presenca': p.id_presenca,
            'data_presenca': p.data_presenca.isoformat(),
            'presente': p.presente
        } for p in presencas]
    })

@presencas_bp.route('/relatorio/diario/<string:data>', methods=['GET'])
def relatorio_diario(data):
    try:
        data_presenca = datetime.strptime(data, '%Y-%m-%d').date()
        
        # Buscar todas as presenças do dia
        presencas = Presenca.query.filter_by(data_presenca=data_presenca).all()
        
        total_alunos = len(presencas)
        presentes = sum(1 for p in presencas if p.presente)
        ausentes = total_alunos - presentes
        
        return jsonify({
            'data': data,
            'total_alunos': total_alunos,
            'presentes': presentes,
            'ausentes': ausentes,
            'percentual_presenca': round((presentes / total_alunos * 100) if total_alunos > 0 else 0, 2),
            'detalhes': [{
                'id_aluno': p.id_aluno,
                'aluno_nome': p.aluno.nome_completo if p.aluno else None,
                'presente': p.presente
            } for p in presencas]
        })
        
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400

@presencas_bp.route('/relatorio/frequencia', methods=['GET'])
def relatorio_frequencia():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({'error': 'Datas de início e fim são obrigatórias'}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        # Buscar frequência por aluno no período
        frequencia_query = db.session.query(
            Presenca.id_aluno,
            func.count(Presenca.id_presenca).label('total_dias'),
            func.sum(func.cast(Presenca.presente, db.Integer)).label('dias_presentes')
        ).filter(
            and_(Presenca.data_presenca >= data_inicio,
                 Presenca.data_presenca <= data_fim)
        ).group_by(Presenca.id_aluno).all()
        
        relatorio = []
        for freq in frequencia_query:
            aluno = Aluno.query.get(freq.id_aluno)
            if aluno:
                dias_ausentes = freq.total_dias - freq.dias_presentes
                percentual = (freq.dias_presentes / freq.total_dias * 100) if freq.total_dias > 0 else 0
                
                relatorio.append({
                    'id_aluno': freq.id_aluno,
                    'aluno_nome': aluno.nome_completo,
                    'total_dias': freq.total_dias,
                    'dias_presentes': freq.dias_presentes,
                    'dias_ausentes': dias_ausentes,
                    'percentual_frequencia': round(percentual, 2)
                })
        
        return jsonify({
            'periodo': f'{data_inicio} a {data_fim}',
            'total_alunos': len(relatorio),
            'frequencia_por_aluno': relatorio
        })
        
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400

@presencas_bp.route('/<int:id_presenca>', methods=['PUT'])
def update_presenca(id_presenca):
    presenca = Presenca.query.get_or_404(id_presenca)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'data_presenca' in data:
            presenca.data_presenca = datetime.strptime(data['data_presenca'], '%Y-%m-%d').date()
        if 'presente' in data:
            presenca.presente = data['presente']
        
        db.session.commit()
        return jsonify({'message': 'Presença atualizada com sucesso'})
        
    except ValueError:
        return jsonify({'error': 'Data de presença inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar presença'}), 500