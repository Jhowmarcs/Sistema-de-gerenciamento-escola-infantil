FROM python:3.9-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o arquivo requirements.txt antes do restante para aproveitar o cache
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação
COPY . .

# Expor a porta do Flask
EXPOSE 5000

# Configuração de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.main

# Comando para iniciar o app com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--log-level", "info", "app.main:app"]