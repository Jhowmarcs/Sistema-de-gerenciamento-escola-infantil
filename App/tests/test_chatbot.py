import pytest
from app.chatbot import process_message, FAQ

def test_process_message_pagamento():
    response = process_message("Qual a data de pagamento?")
    assert response == FAQ["pagamento"]["data"]
    
    response = process_message("Quanto custa a mensalidade?")
    assert response == FAQ["pagamento"]["valor"]

def test_process_message_presenca():
    response = process_message("Como justificar faltas?")
    assert response == FAQ["presenca"]["justificar"]
    
    response = process_message("Como consultar frequência?")
    assert response == FAQ["presenca"]["consultar"]

def test_process_message_default():
    response = process_message("Olá")
    assert "assistente virtual" in response.lower()