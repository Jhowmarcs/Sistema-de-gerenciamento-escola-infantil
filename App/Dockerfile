# Usando Python 3.9 como base
FROM python:3.9-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando os arquivos do projeto
COPY . .

# Instalando as dependências
RUN pip install -r requirements.txt

# Expondo a porta da aplicação Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "-m", "app.main"]
