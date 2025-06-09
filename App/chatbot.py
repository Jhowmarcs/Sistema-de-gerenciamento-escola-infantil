from flask import Blueprint, request, jsonify
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint para o ChatBot
chatbot_bp = Blueprint('chatbot', __name__)

# Dicionário simples de perguntas e respostas
FAQ = {
    "pagamento": {
        "data": "As mensalidades vencem todo dia 10 de cada mês.",
        "valor": "O valor da mensalidade depende do plano escolhido. Por favor, consulte a secretaria para mais detalhes.",
        "como": "Os pagamentos podem ser feitos via boleto bancário, PIX ou diretamente na secretaria da escola."
    },
    "presenca": {
        "justificar": "Para justificar faltas, envie um atestado médico ou uma declaração para o email da escola.",
        "consultar": "Você pode consultar a frequência do seu filho através do sistema online ou entrando em contato com a secretaria."
    },
    "atividade": {
        "proximas": "As próximas atividades estão disponíveis no calendário escolar no sistema.",
        "realizadas": "As atividades já realizadas podem ser consultadas no histórico do aluno no sistema."
    },
    "escola": {
        "horario": "A escola funciona de segunda a sexta, das 7h às 18h.",
        "contato": "Telefone: (XX) XXXX-XXXX, Email: escola@exemplo.com",
        "endereco": "Rua Exemplo, 123 - Bairro - Cidade"
    }
}

@chatbot_bp.route('/', methods=['POST'])
def chat():
    """
    Endpoint principal do ChatBot que recebe perguntas e retorna respostas
    """
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "Mensagem não fornecida"}), 400
    
    user_message = data['message'].lower()
    user_id = data.get('user_id')  # ID do usuário para personalização (opcional)
    
    # Log da interação
    logger.info(f"ChatBot - Mensagem recebida: {user_message} | Usuário: {user_id} | Hora: {datetime.now()}")
    
    # Processamento da mensagem
    response = process_message(user_message, user_id)
    
    return jsonify({"response": response})

def process_message(message, user_id=None):
    """
    Processa a mensagem do usuário e retorna uma resposta apropriada
    """
    # Verificar se a mensagem contém palavras-chave
    if "pagamento" in message or "mensalidade" in message or "valor" in message:
        if "data" in message or "vencimento" in message or "quando" in message:
            return FAQ["pagamento"]["data"]
        elif "valor" in message or "quanto" in message:
            return FAQ["pagamento"]["valor"]
        elif "como" in message or "forma" in message:
            return FAQ["pagamento"]["como"]
        else:
            return FAQ["pagamento"]["data"]
    
    elif "falta" in message or "presença" in message or "frequência" in message:
        if "justificar" in message or "atestado" in message:
            return FAQ["presenca"]["justificar"]
        else:
            return FAQ["presenca"]["consultar"]
    
    elif "atividade" in message or "tarefa" in message:
        if "próxima" in message or "futura" in message:
            return FAQ["atividade"]["proximas"]
        else:
            return FAQ["atividade"]["realizadas"]
    
    elif "horário" in message or "funcionamento" in message:
        return FAQ["escola"]["horario"]
    
    elif "contato" in message or "telefone" in message or "email" in message:
        return FAQ["escola"]["contato"]
    
    elif "endereço" in message or "localização" in message:
        return FAQ["escola"]["endereco"]
    
    else:
        return "Olá! Sou o assistente virtual da escola. Posso ajudar com informações sobre pagamentos, presenças, atividades e informações gerais da escola. Como posso ajudar?"