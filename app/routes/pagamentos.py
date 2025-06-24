from flask import Blueprint, request, jsonify
from app.models import Pagamento, Aluno
from app import db
from datetime import datetime
from sqlalchemy import func, and_

pagamentos_bp = Blueprint('pagamentos', __name__)

@pagamentos_bp.route('/', methods=['GET'])
def get_pagamentos():
    """
    Listar todos os pagamentos
    ---
    tags:
      - Pagamentos
    responses:
      200:
        description: Lista de pagamentos cadastrados
        examples:
          application/json: [
            {
              "id_pagamento": 1,
              "id_aluno": 1,
              "data_pagamento": "2024-05-10",
              "valor_pago": 800.00,
              "forma_pagamento": "Boleto",
              "referencia": "Maio/2024",
              "status": "Pago"
            },
            {
              "id_pagamento": 2,
              "id_aluno": 2,
              "data_pagamento": "2024-05-12",
              "valor_pago": 800.00,
              "forma_pagamento": "Pix",
              "referencia": "Maio/2024",
              "status": "Pendente"
            }
          ]
    """
    pagamentos = Pagamento.query.all()
    return jsonify([{
        'id_pagamento': pagamento.id_pagamento,
        'id_aluno': pagamento.id_aluno,
        'data_pagamento': pagamento.data_pagamento.isoformat(),
        'valor_pago': float(pagamento.valor_pago),
        'forma_pagamento': pagamento.forma_pagamento,
        'referencia': pagamento.referencia,
        'status': pagamento.status
    } for pagamento in pagamentos])

@pagamentos_bp.route('/', methods=['POST'])
def create_pagamento():
    """
    Registrar um novo pagamento
    ---
    tags:
      - Pagamentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id_aluno
            - data_pagamento
            - valor_pago
            - forma_pagamento
            - referencia
            - status
          properties:
            id_aluno:
              type: integer
              example: 1
            data_pagamento:
              type: string
              example: "2024-05-10"
            valor_pago:
              type: number
              example: 800.00
            forma_pagamento:
              type: string
              example: "Boleto"
            referencia:
              type: string
              example: "Maio/2024"
            status:
              type: string
              example: "Pago"
    responses:
      201:
        description: Pagamento registrado com sucesso
        examples:
          application/json: {"message": "Pagamento registrado com sucesso", "id": 3}
      400:
        description: Dados incompletos ou data inválida
        examples:
          application/json: {"error": "Dados incompletos"}
          application/json: {"error": "Data de pagamento inválida"}
      500:
        description: Erro ao registrar pagamento
        examples:
          application/json: {"error": "Erro ao registrar pagamento"}
    """
    data = request.get_json()
    
    required_fields = ['id_aluno', 'data_pagamento', 'valor_pago', 
                      'forma_pagamento', 'referencia', 'status']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
        
        pagamento = Pagamento(
            id_aluno=data['id_aluno'],
            data_pagamento=data_pagamento,
            valor_pago=data['valor_pago'],
            forma_pagamento=data['forma_pagamento'],
            referencia=data['referencia'],
            status=data['status']
        )
        
        db.session.add(pagamento)
        db.session.commit()
        
        return jsonify({'message': 'Pagamento registrado com sucesso', 'id': pagamento.id_pagamento}), 201
        
    except ValueError:
        return jsonify({'error': 'Data de pagamento inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao registrar pagamento'}), 500

@pagamentos_bp.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_pagamentos_aluno(id_aluno):
    """
    Listar pagamentos de um aluno
    ---
    tags:
      - Pagamentos
    parameters:
      - name: id_aluno
        in: path
        type: integer
        required: true
        description: ID do aluno
        example: 1
    responses:
      200:
        description: Lista de pagamentos do aluno
        examples:
          application/json: [
            {
              "id_pagamento": 1,
              "data_pagamento": "2024-05-10",
              "valor_pago": 800.00,
              "forma_pagamento": "Boleto",
              "referencia": "Maio/2024",
              "status": "Pago"
            }
          ]
    """
    pagamentos = Pagamento.query.filter_by(id_aluno=id_aluno).all()
    return jsonify([{
        'id_pagamento': pagamento.id_pagamento,
        'data_pagamento': pagamento.data_pagamento.isoformat(),
        'valor_pago': float(pagamento.valor_pago),
        'forma_pagamento': pagamento.forma_pagamento,
        'referencia': pagamento.referencia,
        'status': pagamento.status
    } for pagamento in pagamentos])

@pagamentos_bp.route('/relatorio/periodo', methods=['GET'])
def relatorio_periodo():
    """
    Relatório de pagamentos por período
    ---
    tags:
      - Pagamentos
    parameters:
      - name: data_inicio
        in: query
        type: string
        required: true
        description: Data de início (YYYY-MM-DD)
        example: "2024-05-01"
      - name: data_fim
        in: query
        type: string
        required: true
        description: Data de fim (YYYY-MM-DD)
        example: "2024-05-31"
    responses:
      200:
        description: Relatório de pagamentos no período
        examples:
          application/json: {
            "periodo": "2024-05-01 a 2024-05-31",
            "total_recebido": 1600.00,
            "total_pendente": 800.00,
            "quantidade_pagamentos": 3,
            "pagamentos": [
              {
                "id_pagamento": 1,
                "id_aluno": 1,
                "data_pagamento": "2024-05-10",
                "valor_pago": 800.00,
                "forma_pagamento": "Boleto",
                "referencia": "Maio/2024",
                "status": "Pago"
              }
            ]
          }
      400:
        description: Datas inválidas
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    if not data_inicio or not data_fim:
        return jsonify({'error': 'Datas de início e fim são obrigatórias'}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        pagamentos = Pagamento.query.filter(
            and_(Pagamento.data_pagamento >= data_inicio,
                 Pagamento.data_pagamento <= data_fim)
        ).all()
        
        total_recebido = sum(float(p.valor_pago) for p in pagamentos if p.status == 'Pago')
        total_pendente = sum(float(p.valor_pago) for p in pagamentos if p.status == 'Pendente')
        
        return jsonify({
            'periodo': f'{data_inicio} a {data_fim}',
            'total_recebido': total_recebido,
            'total_pendente': total_pendente,
            'quantidade_pagamentos': len(pagamentos),
            'pagamentos': [{
                'id_pagamento': p.id_pagamento,
                'id_aluno': p.id_aluno,
                'data_pagamento': p.data_pagamento.isoformat(),
                'valor_pago': float(p.valor_pago),
                'forma_pagamento': p.forma_pagamento,
                'referencia': p.referencia,
                'status': p.status
            } for p in pagamentos]
        })
        
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400

@pagamentos_bp.route('/relatorio/inadimplencia', methods=['GET'])
def relatorio_inadimplencia():
    """
    Relatório de inadimplência
    ---
    tags:
      - Pagamentos
    responses:
      200:
        description: Lista de alunos inadimplentes
        examples:
          application/json: {
            "total_inadimplentes": 1,
            "valor_total_devido": 800.00,
            "inadimplentes": [
              {
                "aluno": "Lucas Pereira",
                "responsavel": "Marina Pereira",
                "telefone": "(11) 91234-5678",
                "email": "marina.pereira@email.com",
                "total_devido": 800.00,
                "pagamentos_pendentes": [
                  {
                    "id_pagamento": 2,
                    "data_pagamento": "2024-05-12",
                    "valor_pago": 800.00,
                    "referencia": "Maio/2024"
                  }
                ]
              }
            ]
          }
    """
    pagamentos_pendentes = Pagamento.query.filter_by(status='Pendente').all()
    
    inadimplentes = {}
    for pagamento in pagamentos_pendentes:
        aluno = Aluno.query.get(pagamento.id_aluno)
        if aluno:
            if aluno.id_aluno not in inadimplentes:
                inadimplentes[aluno.id_aluno] = {
                    'aluno': aluno.nome_completo,
                    'responsavel': aluno.nome_responsavel,
                    'telefone': aluno.telefone_responsavel,
                    'email': aluno.email_responsavel,
                    'total_devido': 0,
                    'pagamentos_pendentes': []
                }
            
            inadimplentes[aluno.id_aluno]['total_devido'] += float(pagamento.valor_pago)
            inadimplentes[aluno.id_aluno]['pagamentos_pendentes'].append({
                'id_pagamento': pagamento.id_pagamento,
                'data_pagamento': pagamento.data_pagamento.isoformat(),
                'valor_pago': float(pagamento.valor_pago),
                'referencia': pagamento.referencia
            })
    
    return jsonify({
        'total_inadimplentes': len(inadimplentes),
        'valor_total_devido': sum(i['total_devido'] for i in inadimplentes.values()),
        'inadimplentes': list(inadimplentes.values())
    })

@pagamentos_bp.route('/<int:id_pagamento>', methods=['PUT'])
def update_pagamento(id_pagamento):
    """
    Atualizar dados de um pagamento
    ---
    tags:
      - Pagamentos
    parameters:
      - name: id_pagamento
        in: path
        type: integer
        required: true
        description: ID do pagamento
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            data_pagamento:
              type: string
              example: "2024-05-10"
            valor_pago:
              type: number
              example: 800.00
            forma_pagamento:
              type: string
              example: "Boleto"
            referencia:
              type: string
              example: "Maio/2024"
            status:
              type: string
              example: "Pago"
    responses:
      200:
        description: Pagamento atualizado com sucesso
        examples:
          application/json: {"message": "Pagamento atualizado com sucesso"}
      400:
        description: Dados não fornecidos ou data inválida
        examples:
          application/json: {"error": "Dados não fornecidos"}
          application/json: {"error": "Data de pagamento inválida"}
      404:
        description: Pagamento não encontrado
      500:
        description: Erro ao atualizar pagamento
        examples:
          application/json: {"error": "Erro ao atualizar pagamento"}
    """
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'data_pagamento' in data:
            pagamento.data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d').date()
        if 'valor_pago' in data:
            pagamento.valor_pago = data['valor_pago']
        if 'forma_pagamento' in data:
            pagamento.forma_pagamento = data['forma_pagamento']
        if 'referencia' in data:
            pagamento.referencia = data['referencia']
        if 'status' in data:
            pagamento.status = data['status']
        
        db.session.commit()
        return jsonify({'message': 'Pagamento atualizado com sucesso'})
        
    except ValueError:
        return jsonify({'error': 'Data de pagamento inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar pagamento'}), 500

@pagamentos_bp.route('/<int:id_pagamento>', methods=['DELETE'])
def delete_pagamento(id_pagamento):
    """
    Excluir um pagamento
    ---
    tags:
      - Pagamentos
    parameters:
      - name: id_pagamento
        in: path
        type: integer
        required: true
        description: ID do pagamento
        example: 1
    responses:
      200:
        description: Pagamento excluído com sucesso
        examples:
          application/json: {"message": "Pagamento excluído com sucesso"}
      404:
        description: Pagamento não encontrado
      500:
        description: Erro ao excluir pagamento
        examples:
          application/json: {"error": "Erro ao excluir pagamento"}
    """
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    try:
        db.session.delete(pagamento)
        db.session.commit()
        return jsonify({'message': 'Pagamento excluído com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir pagamento'}), 500