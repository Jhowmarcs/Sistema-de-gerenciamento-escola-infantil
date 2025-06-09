# Sistema de Gerenciamento Escolar Infantil

Sistema para gerenciamento de escola infantil, incluindo controle de pagamentos, presenças e atividades.

## Requisitos

- Docker e Docker Compose
- Git

## Tecnologias Utilizadas

- Backend: Python 3.9 com Flask
- Banco de Dados: PostgreSQL
- Observabilidade: Prometheus e Grafana
- CI/CD: GitHub Actions
- Containerização: Docker

## Funcionalidades

- Gerenciamento de Alunos
- Gerenciamento de Turmas
- Gerenciamento de Professores
- Controle de Pagamentos
- Controle de Presenças
- Gerenciamento de Atividades
- ChatBot para suporte e informações

## Instalação e Execução

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/sistema-de-gerenciamento-escola-infantil.git
   cd sistema-de-gerenciamento-escola-infantil
   ```

2. Execute o sistema com Docker Compose:
   ```
   docker-compose up -d
   ```

3. Acesse a aplicação:
   - API: http://localhost:5000/api/
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (usuário: admin, senha: admin)

## Estrutura do Projeto

```
.
├── App/                    # Aplicação Flask
│   ├── __init__.py         # Inicialização da aplicação
│   ├── config.py           # Configurações
│   ├── main.py             # Ponto de entrada
│   ├── models.py           # Modelos de dados
│   ├── routes.py           # Rotas da API
│   ├── chatbot.py          # Módulo do ChatBot
│   ├── tests/              # Testes unitários
│   └── requirements.txt    # Dependências
├── BD/                     # Configuração do banco de dados
│   ├── SQL/                # Scripts SQL
│   └── postgresql.conf     # Configuração do PostgreSQL
├── Observabilidade/        # Configuração de monitoramento
│   ├── grafana/            # Dashboards do Grafana
│   └── prometheus/         # Configuração do Prometheus
├── .github/workflows/      # Configuração de CI/CD
└── docker-compose.yml      # Configuração dos containers
```

## Testes

Para executar os testes:

```
cd App
pytest tests/
```

Para gerar relatório de cobertura:

```
cd App
coverage run -m pytest tests/
coverage report
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request