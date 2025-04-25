from datetime import datetime
from app import db  # Importa a instância do SQLAlchemy definida em app/__init__.py
bp = Blueprint('api', __name__)

# -----------------------------------------
# Endpoints para Alunos
# -----------------------------------------
@bp.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    response = []
    for a in alunos:
        response.append({
            'id_aluno': a.id_aluno,
            'nome_completo': a.nome_completo,
            'data_nascimento': a.data_nascimento.strftime('%Y-%m-%d'),
            'id_turma': a.id_turma,
            'nome_responsavel': a.nome_responsavel,
            'telefone_responsavel': a.telefone_responsavel,
            'email_responsavel': a.email_responsavel,
            'informacoes_adicionais': a.informacoes_adicionais
        })
    return jsonify(response), 200

@bp.route('/alunos/<int:id>', methods=['GET'])
def get_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify({
        'id_aluno': aluno.id_aluno,
        'nome_completo': aluno.nome_completo,
        'data_nascimento': aluno.data_nascimento.strftime('%Y-%m-%d'),
        'id_turma': aluno.id_turma,
        'nome_responsavel': aluno.nome_responsavel,
        'telefone_responsavel': aluno.telefone_responsavel,
        'email_responsavel': aluno.email_responsavel,
        'informacoes_adicionais': aluno.informacoes_adicionais
    }), 200

@bp.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.get_json()
    try:
        novo_aluno = Aluno(
            nome_completo = data['nome_completo'],
            data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d'),
            id_turma = data['id_turma'],
            nome_responsavel = data['nome_responsavel'],
            telefone_responsavel = data['telefone_responsavel'],
            email_responsavel = data['email_responsavel'],
            informacoes_adicionais = data.get('informacoes_adicionais')
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno criado com sucesso!', 'id': novo_aluno.id_aluno}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/alunos/<int:id>', methods=['PUT'])
def update_aluno(id):
    data = request.get_json()
    aluno = Aluno.query.get_or_404(id)
    try:
        aluno.nome_completo = data.get('nome_completo', aluno.nome_completo)
        if 'data_nascimento' in data:
            aluno.data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d')
        aluno.id_turma = data.get('id_turma', aluno.id_turma)
        aluno.nome_responsavel = data.get('nome_responsavel', aluno.nome_responsavel)
        aluno.telefone_responsavel = data.get('telefone_responsavel', aluno.telefone_responsavel)
        aluno.email_responsavel = data.get('email_responsavel', aluno.email_responsavel)
        aluno.informacoes_adicionais = data.get('informacoes_adicionais', aluno.informacoes_adicionais)
        db.session.commit()
        return jsonify({'message': 'Aluno atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/alunos/<int:id>', methods=['DELETE'])
def delete_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    try:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'message': 'Aluno removido com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# -----------------------------------------
# Endpoints para Turmas
# -----------------------------------------
@bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    response = [{'id_turma': t.id_turma, 'nome_turma': t.nome_turma, 'id_professor': t.id_professor, 'horario': t.horario} for t in turmas]
    return jsonify(response), 200

@bp.route('/turmas/<int:id>', methods=['GET'])
def get_turma(id):
    turma = Turma.query.get_or_404(id)
    return jsonify({
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    }), 200

@bp.route('/turmas', methods=['POST'])
def create_turma():
    data = request.get_json()
    try:
        nova_turma = Turma(
            nome_turma = data['nome_turma'],
            id_professor = data['id_professor'],
            horario = data['horario']
        )
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify({'message': 'Turma criada com sucesso!', 'id': nova_turma.id_turma}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/turmas/<int:id>', methods=['PUT'])
def update_turma(id):
    data = request.get_json()
    turma = Turma.query.get_or_404(id)
    try:
        turma.nome_turma = data.get('nome_turma', turma.nome_turma)
        turma.id_professor = data.get('id_professor', turma.id_professor)
        turma.horario = data.get('horario', turma.horario)
        db.session.commit()
        return jsonify({'message': 'Turma atualizada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/turmas/<int:id>', methods=['DELETE'])
def delete_turma(id):
    turma = Turma.query.get_or_404(id)
    try:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'message': 'Turma removida com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# -----------------------------------------
# Endpoints para Pagamentos
# -----------------------------------------
@bp.route('/pagamentos', methods=['POST'])
def create_pagamento():
    data = request.get_json()
    try:
        pagamento = Pagamento(
            id_aluno = data['id_aluno'],
            data_pagamento = datetime.strptime(data['data_pagamento'], '%Y-%m-%d') if 'data_pagamento' in data else datetime.today(),
            valor_pago = data['valor_pago'],
            forma_pagamento = data['forma_pagamento'],
            referencia = data['referencia'],
            status = data['status']
        )
        db.session.add(pagamento)
        db.session.commit()
        return jsonify({'message': 'Pagamento registrado com sucesso', 'id': pagamento.id_pagamento}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    pagamentos = Pagamento.query.all()
    response = []
    for p in pagamentos:
        response.append({
            'id_pagamento': p.id_pagamento,
            'id_aluno': p.id_aluno,
            'data_pagamento': p.data_pagamento.strftime('%Y-%m-%d'),
            'valor_pago': float(p.valor_pago),
            'forma_pagamento': p.forma_pagamento,
            'referencia': p.referencia,
            'status': p.status
        })
    return jsonify(response), 200

@bp.route('/pagamentos/<int:id>', methods=['GET'])
def get_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    return jsonify({
        'id_pagamento': pagamento.id_pagamento,
        'id_aluno': pagamento.id_aluno,
        'data_pagamento': pagamento.data_pagamento.strftime('%Y-%m-%d'),
        'valor_pago': float(pagamento.valor_pago),
        'forma_pagamento': pagamento.forma_pagamento,
        'referencia': pagamento.referencia,
        'status': pagamento.status
    }), 200

# -----------------------------------------
# Endpoints para Presenças
# -----------------------------------------
@bp.route('/presencas', methods=['POST'])
def create_presenca():
    data = request.get_json()
    try:
        presenca = Presenca(
            id_aluno = data['id_aluno'],
            data_presenca = datetime.strptime(data['data_presenca'], '%Y-%m-%d') if 'data_presenca' in data else datetime.today(),
            presente = data['presente']
        )
        db.session.add(presenca)
        db.session.commit()
        return jsonify({'message': 'Registro de presença criado com sucesso', 'id': presenca.id_presenca}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/presencas', methods=['GET'])
def get_presencas():
    presencas = Presenca.query.all()
    response = []
    for p in presencas:
        response.append({
            'id_presenca': p.id_presenca,
            'id_aluno': p.id_aluno,
            'data_presenca': p.data_presenca.strftime('%Y-%m-%d'),
            'presente': p.presente
        })
    return jsonify(response), 200

# -----------------------------------------
# Endpoints para Atividades
# -----------------------------------------
@bp.route('/atividades', methods=['POST'])
def create_atividade():
    data = request.get_json()
    try:
        atividade = Atividade(
            descricao = data['descricao'],
            data_realizacao = datetime.strptime(data['data_realizacao'], '%Y-%m-%d')
        )
        db.session.add(atividade)
        db.session.commit()
        return jsonify({'message': 'Atividade criada com sucesso', 'id': atividade.id_atividade}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    response = []
    for a in atividades:
        response.append({
            'id_atividade': a.id_atividade,
            'descricao': a.descricao,
            'data_realizacao': a.data_realizacao.strftime('%Y-%m-%d')
        })
    return jsonify(response), 200

@bp.route('/atividades/<int:id>', methods=['GET'])
def get_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    return jsonify({
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': atividade.data_realizacao.strftime('%Y-%m-%d')
    }), 200

# Endpoint para associar Atividade a Aluno (relação N:N)
@bp.route('/atividade-aluno', methods=['POST'])
def associate_atividade_aluno():
    data = request.get_json()
    try:
        association = AtividadeAluno(
            id_atividade = data['id_atividade'],
            id_aluno = data['id_aluno']
        )
        db.session.add(association)
        db.session.commit()
        return jsonify({'message': 'Atividade associada ao aluno com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# -----------------------------------------
# Endpoints para Usuários e Autenticação
# (Nota: Em produção, implemente hash para senhas e um mecanismo robusto de authenticação)
# -----------------------------------------
@bp.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    try:
        usuario = Usuario(
            login = data['login'],
            senha = data['senha'],  # Use hashing em produção
            nivel_acesso = data['nivel_acesso'],
            id_professor = data.get('id_professor')
        )
        db.session.add(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuário criado com sucesso', 'id': usuario.id_usuario}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    response = []
    for u in usuarios:
        response.append({
            'id_usuario': u.id_usuario,
            'login': u.login,
            'nivel_acesso': u.nivel_acesso,
            'id_professor': u.id_professor
        })
    return jsonify(response), 200

# Exemplo de endpoint de Login (simplificado)
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    login_input = data.get('login')
    senha_input = data.get('senha')
    usuario = Usuario.query.filter_by(login=login_input).first()
    if usuario and usuario.senha == senha_input:
        return jsonify({'message': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401
