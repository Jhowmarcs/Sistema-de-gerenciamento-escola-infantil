from flask import Blueprint, request, jsonify
from app.models import Presenca, Aluno
from app import db
from datetime import datetime
from sqlalchemy import and_, func

presencas_bp = Blueprint('presencas', __name__)

@presencas_bp.route('/', methods=['GET'])
def get_presencas():
    """
    Listar todas as presenças
    ---
    tags:
      - Presenças
    responses:
      200:
        description: Lista de presenças cadastradas
        examples:
          application/json: [
            {
              "id_presenca": 1,
              "id_aluno": 1,
              "data_presenca": "2024-06-10",
              "presente": true
            },
            {
              "id_presenca": 2,
              "id_aluno": 2,
              "data_presenca": "2024-06-10",
              "presente": false
            }
          ]
    """
    presencas = Presenca.query.all()
    return jsonify([{
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': presenca.data_presenca.isoformat(),
        'presente': presenca.presente
    } for presenca in presencas])

@presencas_bp.route('/', methods=['POST'])
def create_presenca():
    """
    Registrar presença de um aluno
    ---
    tags:
      - Presenças
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id_aluno
            - data_presenca
            - presente
          properties:
            id_aluno:
              type: integer
              example: 1
            data_presenca:
              type: string
              example: "2024-06-10"
            presente:
              type: boolean
              example: true
    responses:
      201:
        description: Presença registrada com sucesso
        examples:
          application/json: {"message": "Presença registrada com sucesso", "id": 3}
      400:
        description: Dados incompletos ou data inválida
        examples:
          application/json: {"error": "Dados incompletos"}
          application/json: {"error": "Data de presença inválida"}
      409:
        description: Presença já registrada
        examples:
          application/json: {"error": "Presença já registrada para este aluno nesta data"}
      500:
        description: Erro ao registrar presença
        examples:
          application/json: {"error": "Erro ao registrar presença"}
    """
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
    """
    Listar presenças por data
    ---
    tags:
      - Presenças
    parameters:
      - name: data
        in: path
        type: string
        required: true
        description: Data da presença (YYYY-MM-DD)
        example: "2024-06-10"
    responses:
      200:
        description: Lista de presenças na data
        examples:
          application/json: [
            {
              "id_presenca": 1,
              "id_aluno": 1,
              "presente": true,
              "aluno_nome": "Lucas Pereira"
            }
          ]
      400:
        description: Formato de data inválido
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
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
    """
    Listar presenças de um aluno (com filtro de período)
    ---
    tags:
      - Presenças
    parameters:
      - name: id_aluno
        in: path
        type: integer
        required: true
        description: ID do aluno
        example: 1
      - name: data_inicio
        in: query
        type: string
        required: false
        description: Data de início (YYYY-MM-DD)
        example: "2024-06-01"
      - name: data_fim
        in: query
        type: string
        required: false
        description: Data de fim (YYYY-MM-DD)
        example: "2024-06-30"
    responses:
      200:
        description: Frequência do aluno
        examples:
          application/json: {
            "id_aluno": 1,
            "total_dias": 20,
            "dias_presentes": 18,
            "dias_ausentes": 2,
            "percentual_frequencia": 90.0,
            "presencas": [
              {
                "id_presenca": 1,
                "data_presenca": "2024-06-10",
                "presente": true
              }
            ]
          }
      400:
        description: Formato de data inválido
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
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
    """
    Relatório diário de presenças
    ---
    tags:
      - Presenças
    parameters:
      - name: data
        in: path
        type: string
        required: true
        description: Data do relatório (YYYY-MM-DD)
        example: "2024-06-10"
    responses:
      200:
        description: Relatório diário de presenças
        examples:
          application/json: {
            "data": "2024-06-10",
            "total_alunos": 20,
            "presentes": 18,
            "ausentes": 2,
            "percentual_presenca": 90.0,
            "detalhes": [
              {
                "id_aluno": 1,
                "aluno_nome": "Lucas Pereira",
                "presente": true
              }
            ]
          }
      400:
        description: Formato de data inválido
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
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
    """
    Relatório de frequência por período
    ---
    tags:
      - Presenças
    parameters:
      - name: data_inicio
        in: query
        type: string
        required: true
        description: Data de início (YYYY-MM-DD)
        example: "2024-06-01"
      - name: data_fim
        in: query
        type: string
        required: true
        description: Data de fim (YYYY-MM-DD)
        example: "2024-06-30"
    responses:
      200:
        description: Frequência de todos os alunos no período
        examples:
          application/json: {
            "periodo": "2024-06-01 a 2024-06-30",
            "total_alunos": 2,
            "frequencia_por_aluno": [
              {
                "id_aluno": 1,
                "aluno_nome": "Lucas Pereira",
                "total_dias": 20,
                "dias_presentes": 18,
                "dias_ausentes": 2,
                "percentual_frequencia": 90.0
              }
            ]
          }
      400:
        description: Formato de data inválido ou datas não fornecidas
        examples:
          application/json: {"error": "Formato de data inválido"}
          application/json: {"error": "Datas de início e fim são obrigatórias"}
    """
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
    """
    Atualizar dados de uma presença
    ---
    tags:
      - Presenças
    parameters:
      - name: id_presenca
        in: path
        type: integer
        required: true
        description: ID da presença
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            data_presenca:
              type: string
              example: "2024-06-10"
            presente:
              type: boolean
              example: true
    responses:
      200:
        description: Presença atualizada com sucesso
        examples:
          application/json: {"message": "Presença atualizada com sucesso"}
      400:
        description: Dados não fornecidos ou data inválida
        examples:
          application/json: {"error": "Dados não fornecidos"}
          application/json: {"error": "Data de presença inválida"}
      404:
        description: Presença não encontrada
      500:
        description: Erro ao atualizar presença
        examples:
          application/json: {"error": "Erro ao atualizar presença"}
    """
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

@presencas_bp.route('/<int:id_presenca>', methods=['DELETE'])
def delete_presenca(id_presenca):
    """
    Excluir uma presença
    ---
    tags:
      - Presenças
    parameters:
      - name: id_presenca
        in: path
        type: integer
        required: true
        description: ID da presença
        example: 1
    responses:
      200:
        description: Presença excluída com sucesso
        examples:
          application/json: {"message": "Presença excluída com sucesso"}
      404:
        description: Presença não encontrada
      500:
        description: Erro ao excluir presença
        examples:
          application/json: {"error": "Erro ao excluir presença"}
    """
    presenca = Presenca.query.get_or_404(id_presenca)
    try:
        db.session.delete(presenca)
        db.session.commit()
        return jsonify({'message': 'Presença excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir presença'}), 500