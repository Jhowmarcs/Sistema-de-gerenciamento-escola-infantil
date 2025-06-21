# Sistema de Gerenciamento Escolar Infantil

Sistema completo para gerenciamento de escola infantil desenvolvido em Python com Flask, PostgreSQL e Streamlit.

## 🎯 Funcionalidades

### Módulos Principais
- **Gerenciamento de Alunos**: Cadastro, edição e consulta de informações dos alunos
- **Gerenciamento de Professores**: Controle de professores e suas turmas
- **Gerenciamento de Turmas**: Organização de turmas e horários
- **Controle de Pagamentos**: Registro e acompanhamento de mensalidades
- **Controle de Presenças**: Registro diário de frequência dos alunos
- **Gerenciamento de Atividades**: Cadastro e acompanhamento de atividades pedagógicas
- **ChatBot Inteligente**: Assistente virtual 24/7 para pais e responsáveis

### Relatórios
- Relatórios de pagamentos por período
- Relatórios de inadimplência
- Relatórios de frequência por aluno
- Relatórios de atividades por turma

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.9, Flask, SQLAlchemy
- **Banco de Dados**: PostgreSQL 13
- **Frontend**: Streamlit
- **Containerização**: Docker, Docker Compose
- **Autenticação**: Sistema próprio com níveis de acesso

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.9+ (para desenvolvimento local)
- PostgreSQL (para desenvolvimento local)

## 🚀 Instalação e Execução

### Usando Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Sistema-de-gerenciamento-escola-infantil-main
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

3. Execute com Docker Compose:
```bash
docker-compose up --build
```

4. Acesse as aplicações:
- **API**: http://localhost:5000
- **Frontend**: http://localhost:8501
- **Banco de Dados**: localhost:5432

### Desenvolvimento Local

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure o banco de dados PostgreSQL e execute o script de inicialização:
```bash
psql -U postgres -f database/init.sql
```

3. Configure as variáveis de ambiente no arquivo `.env`

4. Execute a aplicação:
```bash
python app.py
```

5. Execute o frontend (em outro terminal):
```bash
cd frontend
streamlit run streamlit_app.py
```

## 👥 Usuários Padrão

O sistema vem com usuários pré-configurados:

- **Administrador**: 
  - Login: `admin`
  - Senha: `admin123`

- **Secretaria**: 
  - Login: `secretaria`
  - Senha: `sec123`

- **Professores**: 
  - Login: `maria.silva` / Senha: `prof123`
  - Login: `joao.pedro` / Senha: `prof123`
  - Login: `ana.lima` / Senha: `prof123`

## 📊 Estrutura do Banco de Dados

O sistema utiliza as seguintes tabelas principais:

- `usuarios` - Controle de acesso ao sistema
- `professores` - Dados dos professores
- `turmas` - Informações das turmas
- `alunos` - Dados dos alunos matriculados
- `pagamentos` - Controle financeiro
- `presencas` - Registro de frequência
- `atividades` - Atividades pedagógicas
- `atividade_aluno` - Associação entre atividades e alunos

## 🤖 ChatBot

O sistema inclui um ChatBot inteligente que pode responder sobre:

- Informações de pagamentos
- Consulta de presenças
- Atividades realizadas
- Horário de funcionamento
- Informações de contato

### Exemplo de uso da API do ChatBot:

```bash
curl -X POST http://localhost:5000/api/chatbot/mensagem \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Quais são os pagamentos pendentes?", "id_aluno": 1}'
```

## 📱 API Endpoints

### Autenticação
- `POST /api/auth/login` - Login no sistema
- `POST /api/auth/register` - Cadastro de usuário

### Alunos
- `GET /api/alunos` - Listar alunos
- `POST /api/alunos` - Cadastrar aluno
- `GET /api/alunos/{id}` - Buscar aluno específico
- `PUT /api/alunos/{id}` - Atualizar aluno
- `DELETE /api/alunos/{id}` - Excluir aluno

### Pagamentos
- `GET /api/pagamentos` - Listar pagamentos
- `POST /api/pagamentos` - Registrar pagamento
- `GET /api/pagamentos/aluno/{id}` - Pagamentos por aluno
- `GET /api/pagamentos/relatorio/periodo` - Relatório por período
- `GET /api/pagamentos/relatorio/inadimplencia` - Relatório de inadimplência

### Presenças
- `GET /api/presencas` - Listar presenças
- `POST /api/presencas` - Registrar presença
- `GET /api/presencas/data/{data}` - Presenças por data
- `GET /api/presencas/aluno/{id}` - Presenças por aluno
- `GET /api/presencas/relatorio/diario/{data}` - Relatório diário
- `GET /api/presencas/relatorio/frequencia` - Relatório de frequência

### ChatBot
- `POST /api/chatbot/mensagem` - Enviar mensagem
- `GET /api/chatbot/opcoes` - Opções iniciais
- `POST /api/chatbot/transferir` - Transferir atendimento

## 🔒 Níveis de Acesso

- **Administrador**: Acesso completo a todas as funcionalidades
- **Secretaria**: Acesso a cadastros, pagamentos e relatórios
- **Professor**: Acesso a suas turmas, presenças e atividades

## 📈 Monitoramento e Logs

O sistema registra automaticamente:
- Tentativas de login
- Operações de CRUD
- Interações com o ChatBot
- Erros e exceções

## 🧪 Testes

Para executar os testes:

```bash
python -m pytest tests/
```

## 📝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Alexandre Tavares**
- Cliente: Escola Infantil UniFAAT-ADS
- Contato: Alexandre Tavares / Katia

## 🆘 Suporte

Para suporte técnico ou dúvidas sobre o sistema:

1. Consulte a documentação
2. Verifique as issues existentes
3. Crie uma nova issue descrevendo o problema
4. Entre em contato com a equipe de desenvolvimento

---

**Sistema de Gerenciamento Escolar Infantil v1.0**  
Desenvolvido com ❤️ para facilitar a gestão educacional