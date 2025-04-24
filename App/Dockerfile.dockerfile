# Imagem base
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o restante dos arquivos
COPY . .

# Expondo a porta da aplicação
EXPOSE 5000

# Comando para rodar a aplicação com Gunicorn em produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
