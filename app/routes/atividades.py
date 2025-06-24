from flask import Blueprint, request, jsonify
from app.models import Atividade, AtividadeAluno, Aluno, Turma
from app import db
from datetime import datetime
from sqlalchemy import and_

atividades_bp = Blueprint('atividades', __name__)

@atividades_bp.route('/', methods=['GET'])
def get_atividades():
    """
    Listar todas as atividades
    ---
    tags:
      - Atividades
    responses:
      200:
        description: Lista de atividades cadastradas
        examples:
          application/json: [
            {
              "id_atividade": 1,
              "descricao": "Festa Junina",
              "data_realizacao": "2024-06-15",
              "alunos": [
                {"id_aluno": 1, "nome_completo": "Lucas Pereira"},
                {"id_aluno": 2, "nome_completo": "Ana Souza"}
              ]
            }
          ]
    """
    atividades = Atividade.query.all()
    result = []
    
    for atividade in atividades:
        # Buscar alunos associados à atividade
        alunos_atividade = db.session.query(AtividadeAluno, Aluno).join(
            Aluno, AtividadeAluno.id_aluno == Aluno.id_aluno
        ).filter(AtividadeAluno.id_atividade == atividade.id_atividade).all()
        
        result.append({
            'id_atividade': atividade.id_atividade,
            'descricao': atividade.descricao,
            'data_realizacao': atividade.data_realizacao.isoformat(),
            'alunos': [{
                'id_aluno': aluno.id_aluno,
                'nome_completo': aluno.nome_completo
            } for _, aluno in alunos_atividade]
        })
    
    return jsonify(result)

@atividades_bp.route('/', methods=['POST'])
def create_atividade():
    """
    Cadastrar uma nova atividade
    ---
    tags:
      - Atividades
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - descricao
            - data_realizacao
          properties:
            descricao:
              type: string
              example: "Festa Junina"
            data_realizacao:
              type: string
              example: "2024-06-15"
            alunos:
              type: array
              items:
                type: integer
              example: [1, 2]
            id_turma:
              type: integer
              example: 1
    responses:
      201:
        description: Atividade criada com sucesso
        examples:
          application/json: {"message": "Atividade criada com sucesso", "id": 3}
      400:
        description: Dados incompletos ou data inválida
        examples:
          application/json: {"error": "Dados incompletos"}
          application/json: {"error": "Data de realização inválida"}
      500:
        description: Erro ao criar atividade
        examples:
          application/json: {"error": "Erro ao criar atividade"}
    """
    data = request.get_json()
    
    required_fields = ['descricao', 'data_realizacao']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    try:
        data_realizacao = datetime.strptime(data['data_realizacao'], '%Y-%m-%d').date()
        
        atividade = Atividade(
            descricao=data['descricao'],
            data_realizacao=data_realizacao
        )
        
        db.session.add(atividade)
        db.session.flush()  # Para obter o ID da atividade
        
        # Associar alunos à atividade
        if 'alunos' in data and isinstance(data['alunos'], list):
            for id_aluno in data['alunos']:
                atividade_aluno = AtividadeAluno(
                    id_atividade=atividade.id_atividade,
                    id_aluno=id_aluno
                )
                db.session.add(atividade_aluno)
        
        # Associar turma inteira à atividade (se especificado)
        if 'id_turma' in data:
            alunos_turma = Aluno.query.filter_by(id_turma=data['id_turma']).all()
            for aluno in alunos_turma:
                # Verificar se o aluno já não foi adicionado individualmente
                existe = AtividadeAluno.query.filter_by(
                    id_atividade=atividade.id_atividade,
                    id_aluno=aluno.id_aluno
                ).first()
                
                if not existe:
                    atividade_aluno = AtividadeAluno(
                        id_atividade=atividade.id_atividade,
                        id_aluno=aluno.id_aluno
                    )
                    db.session.add(atividade_aluno)
        
        db.session.commit()
        
        return jsonify({'message': 'Atividade criada com sucesso', 'id': atividade.id_atividade}), 201
        
    except ValueError:
        return jsonify({'error': 'Data de realização inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao criar atividade'}), 500

@atividades_bp.route('/<int:id_atividade>', methods=['GET'])
def get_atividade(id_atividade):
    """
    Buscar uma atividade pelo ID
    ---
    tags:
      - Atividades
    parameters:
      - name: id_atividade
        in: path
        type: integer
        required: true
        description: ID da atividade
        example: 1
    responses:
      200:
        description: Dados da atividade
        examples:
          application/json: {
            "id_atividade": 1,
            "descricao": "Festa Junina",
            "data_realizacao": "2024-06-15",
            "alunos": [
              {"id_aluno": 1, "nome_completo": "Lucas Pereira", "turma": "Maternal A"}
            ]
          }
      404:
        description: Atividade não encontrada
    """
    atividade = Atividade.query.get_or_404(id_atividade)
    
    # Buscar alunos associados à atividade
    alunos_atividade = db.session.query(AtividadeAluno, Aluno).join(
        Aluno, AtividadeAluno.id_aluno == Aluno.id_aluno
    ).filter(AtividadeAluno.id_atividade == id_atividade).all()
    
    return jsonify({
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': atividade.data_realizacao.isoformat(),
        'alunos': [{
            'id_aluno': aluno.id_aluno,
            'nome_completo': aluno.nome_completo,
            'turma': aluno.turma.nome_turma if aluno.turma else None
        } for _, aluno in alunos_atividade]
    })

@atividades_bp.route('/aluno/<int:id_aluno>', methods=['GET'])
def get_atividades_aluno(id_aluno):
    """
    Listar atividades de um aluno (com filtro de período)
    ---
    tags:
      - Atividades
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
        description: Lista de atividades do aluno
        examples:
          application/json: {
            "id_aluno": 1,
            "total_atividades": 2,
            "atividades": [
              {"id_atividade": 1, "descricao": "Festa Junina", "data_realizacao": "2024-06-15"}
            ]
          }
      400:
        description: Formato de data inválido
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Buscar atividades do aluno
    query = db.session.query(AtividadeAluno, Atividade).join(
        Atividade, AtividadeAluno.id_atividade == Atividade.id_atividade
    ).filter(AtividadeAluno.id_aluno == id_aluno)
    
    if data_inicio and data_fim:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(
                and_(Atividade.data_realizacao >= data_inicio,
                     Atividade.data_realizacao <= data_fim)
            )
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
    
    atividades_aluno = query.all()
    
    return jsonify({
        'id_aluno': id_aluno,
        'total_atividades': len(atividades_aluno),
        'atividades': [{
            'id_atividade': atividade.id_atividade,
            'descricao': atividade.descricao,
            'data_realizacao': atividade.data_realizacao.isoformat()
        } for _, atividade in atividades_aluno]
    })

@atividades_bp.route('/turma/<int:id_turma>', methods=['GET'])
def get_atividades_turma(id_turma):
    """
    Listar atividades de uma turma (com filtro de período)
    ---
    tags:
      - Atividades
    parameters:
      - name: id_turma
        in: path
        type: integer
        required: true
        description: ID da turma
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
        description: Lista de atividades da turma
        examples:
          application/json: {
            "id_turma": 1,
            "total_atividades": 2,
            "atividades": [
              {"id_atividade": 1, "descricao": "Festa Junina", "data_realizacao": "2024-06-15"}
            ]
          }
      400:
        description: Formato de data inválido
        examples:
          application/json: {"error": "Formato de data inválido"}
    """
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Buscar alunos da turma
    alunos_turma = Aluno.query.filter_by(id_turma=id_turma).all()
    ids_alunos = [aluno.id_aluno for aluno in alunos_turma]
    
    if not ids_alunos:
        return jsonify({
            'id_turma': id_turma,
            'total_atividades': 0,
            'atividades': []
        })
    
    # Buscar atividades dos alunos da turma
    query = db.session.query(Atividade).join(
        AtividadeAluno, Atividade.id_atividade == AtividadeAluno.id_atividade
    ).filter(AtividadeAluno.id_aluno.in_(ids_alunos)).distinct()
    
    if data_inicio and data_fim:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(
                and_(Atividade.data_realizacao >= data_inicio,
                     Atividade.data_realizacao <= data_fim)
            )
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
    
    atividades = query.all()
    
    return jsonify({
        'id_turma': id_turma,
        'total_atividades': len(atividades),
        'atividades': [{
            'id_atividade': atividade.id_atividade,
            'descricao': atividade.descricao,
            'data_realizacao': atividade.data_realizacao.isoformat()
        } for atividade in atividades]
    })

@atividades_bp.route('/relatorio/periodo', methods=['GET'])
def relatorio_atividades_periodo():
    """
    Relatório de atividades por período (e por turma)
    ---
    tags:
      - Atividades
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
      - name: id_turma
        in: query
        type: integer
        required: false
        description: ID da turma (opcional)
        example: 1
    responses:
      200:
        description: Relatório de atividades no período
        examples:
          application/json: {
            "periodo": "2024-06-01 a 2024-06-30",
            "id_turma": 1,
            "total_atividades": 2,
            "atividades": [
              {
                "id_atividade": 1,
                "descricao": "Festa Junina",
                "data_realizacao": "2024-06-15",
                "total_participantes": 20,
                "participantes": [
                  {"id_aluno": 1, "nome_completo": "Lucas Pereira", "turma": "Maternal A"}
                ]
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
    id_turma = request.args.get('id_turma')
    
    if not data_inicio or not data_fim:
        return jsonify({'error': 'Datas de início e fim são obrigatórias'}), 400
    
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        
        query = Atividade.query.filter(
            and_(Atividade.data_realizacao >= data_inicio,
                 Atividade.data_realizacao <= data_fim)
        )
        
        atividades = query.all()
        
        relatorio = []
        for atividade in atividades:
            # Buscar alunos participantes
            alunos_atividade = db.session.query(AtividadeAluno, Aluno).join(
                Aluno, AtividadeAluno.id_aluno == Aluno.id_aluno
            ).filter(AtividadeAluno.id_atividade == atividade.id_atividade).all()
            
            # Filtrar por turma se especificado
            if id_turma:
                alunos_atividade = [(aa, aluno) for aa, aluno in alunos_atividade 
                                   if aluno.id_turma == int(id_turma)]
            
            if not id_turma or alunos_atividade:  # Incluir se não há filtro de turma ou se há alunos da turma
                relatorio.append({
                    'id_atividade': atividade.id_atividade,
                    'descricao': atividade.descricao,
                    'data_realizacao': atividade.data_realizacao.isoformat(),
                    'total_participantes': len(alunos_atividade),
                    'participantes': [{
                        'id_aluno': aluno.id_aluno,
                        'nome_completo': aluno.nome_completo,
                        'turma': aluno.turma.nome_turma if aluno.turma else None
                    } for _, aluno in alunos_atividade]
                })
        
        return jsonify({
            'periodo': f'{data_inicio} a {data_fim}',
            'id_turma': id_turma,
            'total_atividades': len(relatorio),
            'atividades': relatorio
        })
        
    except ValueError:
        return jsonify({'error': 'Formato de data inválido'}), 400

@atividades_bp.route('/<int:id_atividade>', methods=['PUT'])
def update_atividade(id_atividade):
    """
    Atualizar dados de uma atividade
    ---
    tags:
      - Atividades
    parameters:
      - name: id_atividade
        in: path
        type: integer
        required: true
        description: ID da atividade
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
              example: "Festa Junina"
            data_realizacao:
              type: string
              example: "2024-06-15"
            alunos:
              type: array
              items:
                type: integer
              example: [1, 2]
    responses:
      200:
        description: Atividade atualizada com sucesso
        examples:
          application/json: {"message": "Atividade atualizada com sucesso"}
      400:
        description: Dados não fornecidos ou data inválida
        examples:
          application/json: {"error": "Dados não fornecidos"}
          application/json: {"error": "Data de realização inválida"}
      404:
        description: Atividade não encontrada
      500:
        description: Erro ao atualizar atividade
        examples:
          application/json: {"error": "Erro ao atualizar atividade"}
    """
    atividade = Atividade.query.get_or_404(id_atividade)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400
    
    try:
        if 'descricao' in data:
            atividade.descricao = data['descricao']
        if 'data_realizacao' in data:
            atividade.data_realizacao = datetime.strptime(data['data_realizacao'], '%Y-%m-%d').date()
        
        # Atualizar associações com alunos se fornecido
        if 'alunos' in data:
            # Remover associações existentes
            AtividadeAluno.query.filter_by(id_atividade=id_atividade).delete()
            
            # Adicionar novas associações
            for id_aluno in data['alunos']:
                atividade_aluno = AtividadeAluno(
                    id_atividade=id_atividade,
                    id_aluno=id_aluno
                )
                db.session.add(atividade_aluno)
        
        db.session.commit()
        return jsonify({'message': 'Atividade atualizada com sucesso'})
        
    except ValueError:
        return jsonify({'error': 'Data de realização inválida'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar atividade'}), 500

@atividades_bp.route('/<int:id_atividade>', methods=['DELETE'])
def delete_atividade(id_atividade):
    """
    Excluir uma atividade
    ---
    tags:
      - Atividades
    parameters:
      - name: id_atividade
        in: path
        type: integer
        required: true
        description: ID da atividade
        example: 1
    responses:
      200:
        description: Atividade excluída com sucesso
        examples:
          application/json: {"message": "Atividade excluída com sucesso"}
      404:
        description: Atividade não encontrada
      500:
        description: Erro ao excluir atividade
        examples:
          application/json: {"error": "Erro ao excluir atividade"}
    """
    atividade = Atividade.query.get_or_404(id_atividade)
    
    try:
        # Remover associações com alunos primeiro
        AtividadeAluno.query.filter_by(id_atividade=id_atividade).delete()
        
        # Remover a atividade
        db.session.delete(atividade)
        db.session.commit()
        
        return jsonify({'message': 'Atividade excluída com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir atividade'}), 500