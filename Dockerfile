# Dockerfile
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o resto dos arquivos para o container
COPY . .

# Define a porta que será exposta
EXPOSE 5000

# Inicia a aplicação usando Gunicorn para produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
