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

# Comando para iniciar o app
CMD ["python", "-m", "app.main"]
