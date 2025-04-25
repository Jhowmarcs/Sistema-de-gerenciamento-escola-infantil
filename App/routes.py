from flask import Blueprint, request, jsonify
from app.models import db, Aluno, Turma, Professor, Pagamento, Presenca, Atividade, AtividadeAluno, Usuario

bp = Blueprint('routes', __name__)

# -----------------------------------------
# Rota de teste
# -----------------------------------------
@bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API do Sistema de Gerenciamento Escolar Infantil funcionando!"}), 200

# -----------------------------------------
# Endpoints para Alunos
# -----------------------------------------
@bp.route('/alunos', methods=['GET'])
def get_alunos():
    alunos = Aluno.query.all()
    response = [{
        'id_aluno': aluno.id_aluno,
        'nome_completo': aluno.nome_completo,
        'data_nascimento': aluno.data_nascimento.strftime('%Y-%m-%d'),
        'id_turma': aluno.id_turma,
        'nome_responsavel': aluno.nome_responsavel,
        'telefone_responsavel': aluno.telefone_responsavel,
        'email_responsavel': aluno.email_responsavel,
        'informacoes_adicionais': aluno.informacoes_adicionais
    } for aluno in alunos]
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
def cadastrar_aluno():
    dados = request.get_json()
    novo_aluno = Aluno(
        nome_completo=dados.get('nome_completo'),
        data_nascimento=dados.get('data_nascimento'),
        id_turma=dados.get('id_turma'),
        nome_responsavel=dados.get('nome_responsavel'),
        telefone_responsavel=dados.get('telefone_responsavel'),
        email_responsavel=dados.get('email_responsavel'),
        informacoes_adicionais=dados.get('informacoes_adicionais')
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"message": "Aluno cadastrado com sucesso!", "id_aluno": novo_aluno.id_aluno}), 201

@bp.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    dados = request.get_json()
    aluno = Aluno.query.get_or_404(id)
    aluno.nome_completo = dados.get('nome_completo', aluno.nome_completo)
    aluno.data_nascimento = dados.get('data_nascimento', aluno.data_nascimento)
    aluno.id_turma = dados.get('id_turma', aluno.id_turma)
    aluno.nome_responsavel = dados.get('nome_responsavel', aluno.nome_responsavel)
    aluno.telefone_responsavel = dados.get('telefone_responsavel', aluno.telefone_responsavel)
    aluno.email_responsavel = dados.get('email_responsavel', aluno.email_responsavel)
    aluno.informacoes_adicionais = dados.get('informacoes_adicionais', aluno.informacoes_adicionais)
    db.session.commit()
    return jsonify({"message": "Aluno atualizado com sucesso!"}), 200

@bp.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno removido com sucesso!"}), 200


# -----------------------------------------
# Endpoints para Turmas (Exemplo Simples)
# -----------------------------------------
@bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = Turma.query.all()
    response = [{
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    } for turma in turmas]
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
def cadastrar_turma():
    dados = request.get_json()
    nova_turma = Turma(
        nome_turma=dados.get('nome_turma'),
        id_professor=dados.get('id_professor'),
        horario=dados.get('horario')
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({"message": "Turma cadastrada com sucesso!", "id_turma": nova_turma.id_turma}), 201

@bp.route('/turmas/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    dados = request.get_json()
    turma = Turma.query.get_or_404(id)
    turma.nome_turma = dados.get('nome_turma', turma.nome_turma)
    turma.id_professor = dados.get('id_professor', turma.id_professor)
    turma.horario = dados.get('horario', turma.horario)
    db.session.commit()
    return jsonify({"message": "Turma atualizada com sucesso!"}), 200

@bp.route('/turmas/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    turma = Turma.query.get_or_404(id)
    db.session.delete(turma)
    db.session.commit()
    return jsonify({"message": "Turma removida com sucesso!"}), 200

@bp.route('/professores', methods=['GET'])
def get_professores():
    professores = Professor.query.all()
    response = [{
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    } for professor in professores]
    return jsonify(response), 200

@bp.route('/professores/<int:id>', methods=['GET'])
def get_professor(id):
    professor = Professor.query.get_or_404(id)
    return jsonify({
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    }), 200

@bp.route('/professores', methods=['POST'])
def cadastrar_professor():
    dados = request.get_json()
    novo_professor = Professor(
        nome_completo=dados.get('nome_completo'),
        email=dados.get('email'),
        telefone=dados.get('telefone')
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({"message": "Professor cadastrado com sucesso!", "id_professor": novo_professor.id_professor}), 201

@bp.route('/professores/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    dados = request.get_json()
    professor = Professor.query.get_or_404(id)
    professor.nome_completo = dados.get('nome_completo', professor.nome_completo)
    professor.email = dados.get('email', professor.email)
    professor.telefone = dados.get('telefone', professor.telefone)
    db.session.commit()
    return jsonify({"message": "Professor atualizado com sucesso!"}), 200

@bp.route('/professores/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    return jsonify({"message": "Professor removido com sucesso!"}), 200

@bp.route('/pagamentos', methods=['GET'])
def get_pagamentos():
    pagamentos = Pagamento.query.all()
    response = [{
        'id_pagamento': pagamento.id_pagamento,
        'id_aluno': pagamento.id_aluno,
        'data_pagamento': pagamento.data_pagamento.strftime('%Y-%m-%d'),
        'valor_pago': float(pagamento.valor_pago),
        'forma_pagamento': pagamento.forma_pagamento,
        'referencia': pagamento.referencia,
        'status': pagamento.status
    } for pagamento in pagamentos]
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

@bp.route('/pagamentos', methods=['POST'])
def cadastrar_pagamento():
    dados = request.get_json()
    novo_pagamento = Pagamento(
        id_aluno=dados.get('id_aluno'),
        data_pagamento=dados.get('data_pagamento'),
        valor_pago=dados.get('valor_pago'),
        forma_pagamento=dados.get('forma_pagamento'),
        referencia=dados.get('referencia'),
        status=dados.get('status')
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify({"message": "Pagamento registrado com sucesso!", "id_pagamento": novo_pagamento.id_pagamento}), 201

@bp.route('/pagamentos/<int:id>', methods=['PUT'])
def atualizar_pagamento(id):
    dados = request.get_json()
    pagamento = Pagamento.query.get_or_404(id)
    pagamento.id_aluno = dados.get('id_aluno', pagamento.id_aluno)
    pagamento.data_pagamento = dados.get('data_pagamento', pagamento.data_pagamento)
    pagamento.valor_pago = dados.get('valor_pago', pagamento.valor_pago)
    pagamento.forma_pagamento = dados.get('forma_pagamento', pagamento.forma_pagamento)
    pagamento.referencia = dados.get('referencia', pagamento.referencia)
    pagamento.status = dados.get('status', pagamento.status)
    db.session.commit()
    return jsonify({"message": "Pagamento atualizado com sucesso!"}), 200

@bp.route('/pagamentos/<int:id>', methods=['DELETE'])
def deletar_pagamento(id):
    pagamento = Pagamento.query.get_or_404(id)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({"message": "Pagamento removido com sucesso!"}), 200

@bp.route('/presencas', methods=['GET'])
def get_presencas():
    presencas = Presenca.query.all()
    response = [{
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': presenca.data_presenca.strftime('%Y-%m-%d'),
        'presente': presenca.presente
    } for presenca in presencas]
    return jsonify(response), 200

@bp.route('/presencas/<int:id>', methods=['GET'])
def get_presenca(id):
    presenca = Presenca.query.get_or_404(id)
    return jsonify({
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': presenca.data_presenca.strftime('%Y-%m-%d'),
        'presente': presenca.presente
    }), 200

@bp.route('/presencas', methods=['POST'])
def registrar_presenca():
    dados = request.get_json()
    nova_presenca = Presenca(
        id_aluno=dados.get('id_aluno'),
        data_presenca=dados.get('data_presenca'),
        presente=dados.get('presente')
    )
    db.session.add(nova_presenca)
    db.session.commit()
    return jsonify({"message": "Presença registrada com sucesso!", "id_presenca": nova_presenca.id_presenca}), 201

@bp.route('/presencas/<int:id>', methods=['DELETE'])
def deletar_presenca(id):
    presenca = Presenca.query.get_or_404(id)
    db.session.delete(presenca)
    db.session.commit()
    return jsonify({"message": "Presença removida com sucesso!"}), 200

@bp.route('/atividades', methods=['GET'])
def get_atividades():
    atividades = Atividade.query.all()
    response = [{
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': atividade.data_realizacao.strftime('%Y-%m-%d')
    } for atividade in atividades]
    return jsonify(response), 200

@bp.route('/atividades/<int:id>', methods=['GET'])
def get_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    return jsonify({
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': atividade.data_realizacao.strftime('%Y-%m-%d')
    }), 200

@bp.route('/atividades', methods=['POST'])
def cadastrar_atividade():
    dados = request.get_json()
    nova_atividade = Atividade(
        descricao=dados.get('descricao'),
        data_realizacao=dados.get('data_realizacao')
    )
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify({"message": "Atividade cadastrada com sucesso!", "id_atividade": nova_atividade.id_atividade}), 201

@bp.route('/atividades/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    dados = request.get_json()
    atividade = Atividade.query.get_or_404(id)
    atividade.descricao = dados.get('descricao', atividade.descricao)
    atividade.data_realizacao = dados.get('data_realizacao', atividade.data_realizacao)
    db.session.commit()
    return jsonify({"message": "Atividade atualizada com sucesso!"}), 200

@bp.route('/atividades/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade removida com sucesso!"}), 200

@bp.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    novo_usuario = Usuario(
        login=dados.get('login'),
        senha=dados.get('senha'),  # Em produção, utilize hashing para senhas!
        nivel_acesso=dados.get('nivel_acesso'),
        id_professor=dados.get('id_professor')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário cadastrado com sucesso!", "id_usuario": novo_usuario.id_usuario}), 201


@bp.route('/login', methods=['POST'])
def autenticar_usuario():
    dados = request.get_json()
    login = dados.get('login')
    senha = dados.get('senha')  # Em produção, verifique hash de senha!

    # Busca o usuário no banco de dados
    usuario = Usuario.query.filter_by(login=login).first()

    if usuario and usuario.senha == senha:  # Em produção, use comparação de hash.
        return jsonify({"message": "Login realizado com sucesso!", "id_usuario": usuario.id_usuario}), 200
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401


# Adicione CRUDs completos para Turmas, Professores, etc., aqui!
