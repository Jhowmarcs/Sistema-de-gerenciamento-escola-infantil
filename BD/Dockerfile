FROM postgres:13

# Copiar arquivos de configuração
COPY postgresql.conf /etc/postgresql/postgresql.conf

# Copiar scripts SQL para inicialização
COPY SQL/create_tables.sql /docker-entrypoint-initdb.d/

# Expor a porta padrão do PostgreSQL
EXPOSE 5432

# Comando para iniciar o PostgreSQL com a configuração personalizada
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]