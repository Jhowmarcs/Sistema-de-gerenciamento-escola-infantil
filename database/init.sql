-- Script de inicialização do banco de dados
-- Sistema de Gerenciamento Escolar Infantil

-- Tabela de Professores
CREATE TABLE IF NOT EXISTS professores (
    id_professor SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Turmas
CREATE TABLE IF NOT EXISTS turmas (
    id_turma SERIAL PRIMARY KEY,
    nome_turma VARCHAR(50) NOT NULL,
    id_professor INTEGER NOT NULL,
    horario VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor) ON DELETE CASCADE
);

-- Tabela de Alunos
CREATE TABLE IF NOT EXISTS alunos (
    id_aluno SERIAL PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE NOT NULL,
    id_turma INTEGER NOT NULL,
    nome_responsavel VARCHAR(255) NOT NULL,
    telefone_responsavel VARCHAR(20) NOT NULL,
    email_responsavel VARCHAR(100) NOT NULL,
    informacoes_adicionais TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_turma) REFERENCES turmas(id_turma) ON DELETE CASCADE
);

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nivel_acesso VARCHAR(20) NOT NULL CHECK (nivel_acesso IN ('administrador', 'secretaria', 'professor')),
    id_professor INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_professor) REFERENCES professores(id_professor) ON DELETE SET NULL
);

-- Tabela de Pagamentos
CREATE TABLE IF NOT EXISTS pagamentos (
    id_pagamento SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    data_pagamento DATE NOT NULL,
    valor_pago DECIMAL(10, 2) NOT NULL,
    forma_pagamento VARCHAR(50) NOT NULL,
    referencia VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pago', 'Pendente')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE
);

-- Tabela de Presenças
CREATE TABLE IF NOT EXISTS presencas (
    id_presenca SERIAL PRIMARY KEY,
    id_aluno INTEGER NOT NULL,
    data_presenca DATE NOT NULL,
    presente BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE,
    UNIQUE(id_aluno, data_presenca)
);

-- Tabela de Atividades
CREATE TABLE IF NOT EXISTS atividades (
    id_atividade SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_realizacao DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Associação Atividade-Aluno (N:N)
CREATE TABLE IF NOT EXISTS atividade_aluno (
    id_atividade INTEGER NOT NULL,
    id_aluno INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_atividade, id_aluno),
    FOREIGN KEY (id_atividade) REFERENCES atividades(id_atividade) ON DELETE CASCADE,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno) ON DELETE CASCADE
);

-- Índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_alunos_turma ON alunos(id_turma);
CREATE INDEX IF NOT EXISTS idx_pagamentos_aluno ON pagamentos(id_aluno);
CREATE INDEX IF NOT EXISTS idx_pagamentos_status ON pagamentos(status);
CREATE INDEX IF NOT EXISTS idx_pagamentos_data ON pagamentos(data_pagamento);
CREATE INDEX IF NOT EXISTS idx_presencas_aluno ON presencas(id_aluno);
CREATE INDEX IF NOT EXISTS idx_presencas_data ON presencas(data_presenca);
CREATE INDEX IF NOT EXISTS idx_atividades_data ON atividades(data_realizacao);

-- Dados iniciais de exemplo
INSERT INTO professores (nome_completo, email, telefone) VALUES
('Maria Silva Santos', 'maria.silva@unifaat.edu.br', '(11) 99999-0001'),
('João Pedro Oliveira', 'joao.pedro@unifaat.edu.br', '(11) 99999-0002'),
('Ana Carolina Lima', 'ana.lima@unifaat.edu.br', '(11) 99999-0003')
ON CONFLICT DO NOTHING;

INSERT INTO turmas (nome_turma, id_professor, horario) VALUES
('Maternal I', 1, 'Manhã - 07:00 às 12:00'),
('Maternal II', 2, 'Tarde - 13:00 às 18:00'),
('Jardim I', 3, 'Integral - 07:00 às 19:00')
ON CONFLICT DO NOTHING;

INSERT INTO usuarios (login, senha, nivel_acesso, id_professor) VALUES
('admin', 'admin123', 'administrador', NULL),
('secretaria', 'sec123', 'secretaria', NULL),
('maria.silva', 'prof123', 'professor', 1),
('joao.pedro', 'prof123', 'professor', 2),
('ana.lima', 'prof123', 'professor', 3)
ON CONFLICT (login) DO NOTHING;