from datetime import datetime
from app import db  # Importa a instância do SQLAlchemy definida em app/__init__.py

# Modelo para Alunos
class Aluno(db.Model):
    __tablename__ = 'alunos'
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    id_turma = db.Column(db.Integer, db.ForeignKey('turmas.id_turma'), nullable=False)
    nome_responsavel = db.Column(db.String(255), nullable=False)
    telefone_responsavel = db.Column(db.String(20), nullable=False)
    email_responsavel = db.Column(db.String(100), nullable=False)
    informacoes_adicionais = db.Column(db.Text, nullable=True)
    # Relacionamentos
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)
    presencas = db.relationship('Presenca', backref='aluno', lazy=True)
    atividades = db.relationship('Atividade', secondary='atividade_aluno', backref='alunos', lazy=True)

# Modelo para Turmas
class Turma(db.Model):
    __tablename__ = 'turmas'
    id_turma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_turma = db.Column(db.String(50), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=False)
    horario = db.Column(db.String(100), nullable=False)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

# Modelo para Professores
class Professor(db.Model):
    __tablename__ = 'professores'
    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    usuario = db.relationship('Usuario', backref='professor', uselist=False)

# Modelo para Pagamentos
class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    referencia = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Modelo para Presenças
class Presenca(db.Model):
    __tablename__ = 'presencas'
    id_presenca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), nullable=False)
    data_presenca = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

# Modelo para Atividades
class Atividade(db.Model):
    __tablename__ = 'atividades'
    id_atividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.Text, nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)

# Modelo para Associação entre Atividades e Alunos (N:N)
class AtividadeAluno(db.Model):
    __tablename__ = 'atividade_aluno'
    id_atividade = db.Column(db.Integer, db.ForeignKey('atividades.id_atividade'), primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id_aluno'), primary_key=True)

# Modelo para Usuários (para autenticação)
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # Hash a senha em produção!
    nivel_acesso = db.Column(db.String(20), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professores.id_professor'), nullable=True)
