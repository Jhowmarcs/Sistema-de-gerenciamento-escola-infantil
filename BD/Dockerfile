# BD/Dockerfile

FROM postgres:13

# Define variáveis de ambiente padrão (ajuste conforme necessário)
ENV POSTGRES_USER=usuario
ENV POSTGRES_PASSWORD=senha
ENV POSTGRES_DB=nome_banco

# Copia os scripts SQL para a pasta de inicialização do PostgreSQL
# Todos os scripts nessa pasta serão executados na criação do container
COPY SQL/ /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432
