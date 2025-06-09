import logging
from functools import wraps
from flask import request, jsonify, current_app
import re

# Configuração de logging
logger = logging.getLogger(__name__)

def validate_email(email):
    """Valida o formato de um endereço de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valida o formato de um número de telefone."""
    # Remove caracteres não numéricos
    phone_digits = re.sub(r'\D', '', phone)
    # Verifica se tem entre 10 e 11 dígitos (com ou sem DDD)
    return 10 <= len(phone_digits) <= 11

def log_request(f):
    """Decorator para logar requisições à API."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        logger.info(f"Requisição {request.method} para {request.path} de {request.remote_addr}")
        return f(*args, **kwargs)
    return decorated_function

def format_error(message, status_code=400):
    """Formata mensagens de erro para a API."""
    return jsonify({"error": message}), status_code

def format_success(data=None, message=None, status_code=200):
    """Formata mensagens de sucesso para a API."""
    response = {}
    if data is not None:
        response["data"] = data
    if message is not None:
        response["message"] = message
    return jsonify(response), status_code