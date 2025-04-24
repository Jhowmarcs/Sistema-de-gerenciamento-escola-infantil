-- BD/SQL/create_tables.sql

-- Tabela Aluno
CREATE TABLE alunos (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INTEGER NOT NULL,
    nome_responsavel VARCHAR(255) NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    email_responsavel VARCHAR(100) NOT NULL,
    informacoes_adicionais TEXT,
    CONSTRAINT fk_turma FOREIGN KEY (id_turma) REFERENCES turmas(id_turma)
);

-- Tabela Turma
CREATE TABLE turmas (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INTEGER NOT NULL,
    horario VARCHAR(100) NOT NULL,
    CONSTRAINT fk_professor FOREIGN KEY (id_professor) REFERENCES professores(id_professor)
);

-- Tabela Professor
CREATE TABLE professores (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL
);

-- Tabela Pagamento
CREATE TABLE pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10,2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    referencia VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    CONSTRAINT fk_pagamento_aluno FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

-- Tabela Presenca
CREATE TABLE presencas (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    data_presenca DATE NOT NULL,
    presente BOOLEAN NOT NULL,
    CONSTRAINT fk_presenca_aluno FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

-- Tabela Atividade
CREATE TABLE atividades (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL
);

-- Tabela Atividade_Aluno - Ligação N:N
CREATE TABLE atividade_aluno (
    id_atividade INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    PRIMARY KEY (id_atividade, id_aluno),
    CONSTRAINT fk_atividade FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade),
    CONSTRAINT fk_aluno FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

-- Tabela Usuario
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20) NOT NULL,
    id_professor INTEGER,
    CONSTRAINT fk_usuario_professor FOREIGN KEY (id_professor) REFERENCES professores(id_professor)
);
