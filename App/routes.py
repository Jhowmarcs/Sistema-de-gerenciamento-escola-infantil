from flask import Blueprint, request, jsonify
from app.models import db, Aluno

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "API do Sistema de Gerenciamento Escolar Infantil funcionando!"})

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
    return jsonify({"message": "Aluno cadastrado com sucesso!"}), 201
