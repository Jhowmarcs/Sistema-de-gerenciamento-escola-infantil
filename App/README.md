# Módulo de Aplicação - Sistema de Gerenciamento Escolar Infantil

## Finalidade do Módulo

Este módulo contém o código principal do back-end, desenvolvido com Flask, que implementa a API e integra a modelagem dos dados conforme o MER definido para o sistema de gerenciamento escolar infantil. Aqui estão definidas as rotas, os modelos de dados (por exemplo, Aluno, Turma, Professor, Pagamento, etc.) e a configuração da conexão com o banco de dados. O objetivo é fornecer uma base escalável e modular para gerenciar as funcionalidades escolares (cadastro, pagamentos, presenças, atividades e integração com o ChatBot) de forma organizada e facilitada.

## Requisitos

- **Python 3.10** ou superior.
- **Virtualenv** (para isolamento do ambiente, recomendado).
- Dependências listadas no arquivo `requirements.txt` (ex.: Flask, Flask-SQLAlchemy, Gunicorn).
- (Opcional) **Docker** e **Docker Compose**, caso opte por executar a aplicação em containers.

## Configuração do Ambiente

### 1. Clonando o Repositório

Caso ainda não tenha clonado o repositório, execute:

```bash
git clone <URL_DO_REPOSITORIO>
cd Sistema_de_gerenciamento_escolar/app


2. Criando e Ativando o Ambiente Virtual
No Windows (PowerShell):

powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
(Se houver problema com a política de execução, ajuste com:)

powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
No Windows (CMD):

cmd
python -m venv venv
venv\Scripts\activate
No Linux/Mac:

bash
python3 -m venv venv
source venv/bin/activate
Após a ativação, você verá o nome do ambiente (ex: (venv)) no prompt.

3. Instalando as Dependências
Com o ambiente virtual ativo, instale as dependências definidas:

bash
pip install -r ../requirements.txt
4. Configuração de Variáveis de Ambiente
Recomenda-se configurar variáveis de ambiente para parâmetros sensíveis, como a URL do banco de dados. Você poderá, por exemplo, utilizar um arquivo .env e uma ferramenta como o python-dotenv para carregá-las na aplicação.

Como Rodar a Aplicação
Executando Localmente com Python
Garanta que o ambiente virtual esteja ativo.

No diretório app/, execute o arquivo principal:

bash
python main.py
A aplicação iniciará o servidor Flask na porta 5000 (acessível via http://localhost:5000). A rota raíz (/) retornará uma mensagem indicando que a API está em funcionamento.

Executando a Aplicação com Docker
Esta aplicação já possui um Dockerfile que facilita a execução em container.

Certifique-se de ter o Docker e o Docker Compose instalados.

A partir da raiz do projeto (onde está o arquivo docker-compose.yaml), execute:

bash
docker-compose up --build
O container da aplicação será iniciado e estará acessível na porta 5000 conforme definida no mapeamento do docker-compose.yaml.

Estrutura do Módulo (app/)
plaintext
Sistema_de_gerenciamento_escolar/
└── app/
    ├── Dockerfile          # Instruções para criar e configurar o container da aplicação
    ├── README.md           # Documentação deste módulo (este arquivo)
    ├── __init__.py         # Inicializa a aplicação e configura o banco de dados (Flask SQLAlchemy)
    ├── config.py           # Configurações da aplicação (ex.: conexão com o PostgreSQL)
    ├── models.py           # Modelagem dos dados conforme o MER (Aluno, Turma, etc.)
    ├── routes.py           # Definição dos endpoints REST da API
    └── main.py             # Arquivo principal para execução da aplicação
Observações
Modo de Desenvolvimento: Para facilitar o desenvolvimento, é possível rodar a aplicação com o modo debug habilitado. No entanto, para produção, desative o debug e configure corretamente as variáveis de ambiente.

Containerização: Utilizar Docker garante a padronização do ambiente de desenvolvimento, testes e produção, evitando problemas causados por diferenças de configuração entre máquinas.

Testes e Integração: É recomendável criar casos de teste para as rotas e validações de dados. Você pode expandir a estrutura adicionando a pasta tests/ para testes unitários e de integração.

Caso precise de mais detalhes ou ajudas, consulte a documentação geral do projeto ou entre em contato com a equipe de desenvolvimento.

