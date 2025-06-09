# Módulo BD - Banco de Dados

Este módulo contém os scripts SQL necessários para criar a estrutura do banco de dados do Sistema de Gerenciamento Escolar Infantil conforme o Modelo Entidade-Relacionamento (MER) fornecido.

## Estrutura do Módulo

- **Dockerfile**: Utilizado para construir uma imagem personalizada do PostgreSQL que automaticamente executa os scripts de inicialização.
- **SQL/**: Pasta contendo os scripts:
  - `create_tables.sql`: Comandos para a criação das tabelas.
  - `inserts.sql` (opcional): Scripts de inserção de dados iniciais.

## Como Funciona

Ao construir o container a partir deste Dockerfile, a imagem do PostgreSQL copia os scripts presentes em `BD/SQL/` para o diretório `/docker-entrypoint-initdb.d/`. O PostgreSQL executa automaticamente todos os scripts contidos nessa pasta no momento da criação do container (caso o volume do banco de dados esteja vazio).

## Executando o Container

O arquivo `docker-compose.yaml` (localizado na raiz do projeto) está configurado para utilizar esta imagem. Basta executar:

```bash
docker-compose up --build
