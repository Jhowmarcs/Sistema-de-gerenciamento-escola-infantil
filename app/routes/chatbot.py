from flask import Blueprint, request, jsonify
from app.models import Aluno, Pagamento, Presenca, Atividade, AtividadeAluno
from app import db
from datetime import datetime, date
import re

chatbot_bp = Blueprint('chatbot', __name__)

class ChatBot:
    def __init__(self):
        self.responses = {
            'saudacao': [
                'olá', 'oi', 'bom dia', 'boa tarde', 'boa noite', 'hey', 'e aí', 'saudações', 'salve', 'tudo bem', 'como vai', 'fala', 'opa', 'alô', 'hello', 'hi'
            ],
            'pagamento': [
                'pagamento', 'mensalidade', 'valor', 'quanto', 'pagar', 'boleto', 'taxa', 'cobrança', 'fatura', 'parcelamento', 'desconto', 'vencimento', 'atraso', 'quitar', 'pagou', 'pagarei', 'pix', 'cartão', 'dinheiro', 'transferência', 'comprovante'
            ],
            'presenca': [
                'presença', 'falta', 'frequência', 'ausência', 'compareceu', 'veio', 'faltou', 'presente', 'ausente', 'justificar', 'atraso', 'adiantamento', 'pontualidade', 'faltas', 'presenças'
            ],
            'atividade': [
                'atividade', 'tarefa', 'exercício', 'trabalho', 'projeto', 'lição', 'prova', 'avaliação', 'atividade extra', 'atividade complementar', 'atividade pedagógica', 'atividade escolar', 'atividade do dia', 'atividade da semana', 'atividade recente', 'atividade passada', 'atividade futura'
            ],
            'horario': [
                'horário', 'funcionamento', 'abre', 'fecha', 'hora', 'expediente', 'abertura', 'fechamento', 'turno', 'manhã', 'tarde', 'noite', 'agenda', 'calendário', 'dias', 'quando abre', 'quando fecha'
            ],
            'contato': [
                'contato', 'telefone', 'email', 'falar', 'conversar', 'whatsapp', 'zap', 'mensagem', 'atendimento', 'secretaria', 'direção', 'diretor', 'coordenador', 'coordenação', 'ajuda', 'suporte', 'informação', 'informações', 'endereço', 'localização', 'onde fica', 'visita', 'agendar', 'reunião', 'marcar', 'encontro'
            ]
        }
    
    def processar_mensagem(self, mensagem, id_aluno=None):
        mensagem = mensagem.lower().strip()
        # Mapeamento direto das opções sugeridas para funções
        opcoes_map = {
            'consultar pagamentos': lambda: self._resposta_pagamento(mensagem, id_aluno),
            'verificar presenças': lambda: self._resposta_presenca(mensagem, id_aluno),
            'ver atividades': lambda: self._resposta_atividade(mensagem, id_aluno),
            'horário de funcionamento': self._resposta_horario,
            'informações de contato': self._resposta_contato,
            'falar com atendente': self._resposta_contato,
            'agendar reunião': self._resposta_contato,
            'falar com a direção': self._resposta_contato,
            'secretaria': self._resposta_contato
        }
        if mensagem in opcoes_map:
            return opcoes_map[mensagem]()
        
        # Saudação
        if any(palavra in mensagem for palavra in self.responses['saudacao']):
            return self._resposta_saudacao()
        
        # Perguntas sobre pagamento
        if any(palavra in mensagem for palavra in self.responses['pagamento']):
            return self._resposta_pagamento(mensagem, id_aluno)
        
        # Perguntas sobre presença
        if any(palavra in mensagem for palavra in self.responses['presenca']):
            return self._resposta_presenca(mensagem, id_aluno)
        
        # Perguntas sobre atividades
        if any(palavra in mensagem for palavra in self.responses['atividade']):
            return self._resposta_atividade(mensagem, id_aluno)
        
        # Perguntas sobre horário
        if any(palavra in mensagem for palavra in self.responses['horario']):
            return self._resposta_horario()
        
        # Perguntas sobre contato
        if any(palavra in mensagem for palavra in self.responses['contato']):
            return self._resposta_contato()
        
        # Se nenhuma regra for satisfeita, retorna resposta padrão
        return self._resposta_padrao()
    
    def _resposta_saudacao(self):
        return {
            'resposta': 'Olá! Sou o assistente virtual da Escola Infantil UniFAAT-ADS. Como posso ajudá-lo hoje?',
            'opcoes': [
                'Consultar pagamentos',
                'Verificar presenças',
                'Ver atividades',
                'Horário de funcionamento',
                'Informações de contato'
            ]
        }
    
    def _resposta_pagamento(self, mensagem, id_aluno):
        if id_aluno:
            try:
                aluno = Aluno.query.get(id_aluno)
                if not aluno:
                    return {'resposta': 'Aluno não encontrado.'}
                
                # Buscar pagamentos pendentes
                pagamentos_pendentes = Pagamento.query.filter_by(
                    id_aluno=id_aluno, 
                    status='Pendente'
                ).all()
                
                if pagamentos_pendentes:
                    total_devido = sum(float(p.valor_pago) for p in pagamentos_pendentes)
                    resposta = f"Olá! Encontrei {len(pagamentos_pendentes)} pagamento(s) pendente(s) para {aluno.nome_completo}:\n\n"
                    
                    for pagamento in pagamentos_pendentes:
                        resposta += f"• {pagamento.referencia}: R$ {pagamento.valor_pago:.2f} (Vencimento: {pagamento.data_pagamento})\n"
                    
                    resposta += f"\nTotal devido: R$ {total_devido:.2f}"
                    
                    return {
                        'resposta': resposta,
                        'dados': {
                            'total_pendente': total_devido,
                            'quantidade': len(pagamentos_pendentes)
                        }
                    }
                else:
                    return {'resposta': f'Ótimas notícias! Não há pagamentos pendentes para {aluno.nome_completo}.'}
                    
            except Exception as e:
                return {'resposta': 'Erro ao consultar informações de pagamento. Tente novamente mais tarde.'}
        else:
            return {
                'resposta': 'Para consultar informações específicas de pagamento, preciso saber qual aluno. Os pagamentos podem ser realizados até o dia 10 de cada mês via PIX, cartão ou dinheiro na secretaria.',
                'opcoes': ['Como fazer um pagamento?', 'Formas de pagamento aceitas']
            }
    
    def _resposta_presenca(self, mensagem, id_aluno):
        if id_aluno:
            try:
                aluno = Aluno.query.get(id_aluno)
                if not aluno:
                    return {'resposta': 'Aluno não encontrado.'}
                
                # Buscar presenças do mês atual
                hoje = date.today()
                inicio_mes = hoje.replace(day=1)
                
                presencas_mes = Presenca.query.filter(
                    Presenca.id_aluno == id_aluno,
                    Presenca.data_presenca >= inicio_mes,
                    Presenca.data_presenca <= hoje
                ).all()
                
                if presencas_mes:
                    total_dias = len(presencas_mes)
                    dias_presentes = sum(1 for p in presencas_mes if p.presente)
                    percentual = (dias_presentes / total_dias * 100) if total_dias > 0 else 0
                    
                    resposta = f"Frequência de {aluno.nome_completo} neste mês:\n\n"
                    resposta += f"• Total de dias letivos: {total_dias}\n"
                    resposta += f"• Dias presentes: {dias_presentes}\n"
                    resposta += f"• Dias ausentes: {total_dias - dias_presentes}\n"
                    resposta += f"• Percentual de frequência: {percentual:.1f}%"
                    
                    return {
                        'resposta': resposta,
                        'dados': {
                            'percentual_frequencia': percentual,
                            'dias_presentes': dias_presentes,
                            'total_dias': total_dias
                        }
                    }
                else:
                    return {'resposta': f'Ainda não há registros de presença para {aluno.nome_completo} neste mês.'}
                    
            except Exception as e:
                return {'resposta': 'Erro ao consultar informações de presença. Tente novamente mais tarde.'}
        else:
            return {
                'resposta': 'Para consultar a frequência específica, preciso saber qual aluno. Em caso de faltas, é importante justificar na secretaria.',
                'opcoes': ['Como justificar uma falta?', 'Política de frequência']
            }
    
    def _resposta_atividade(self, mensagem, id_aluno):
        if id_aluno:
            try:
                aluno = Aluno.query.get(id_aluno)
                if not aluno:
                    return {'resposta': 'Aluno não encontrado.'}
                
                # Buscar atividades recentes (últimos 7 dias)
                data_limite = date.today() - datetime.timedelta(days=7)
                
                atividades_recentes = db.session.query(Atividade).join(
                    AtividadeAluno, Atividade.id_atividade == AtividadeAluno.id_atividade
                ).filter(
                    AtividadeAluno.id_aluno == id_aluno,
                    Atividade.data_realizacao >= data_limite
                ).all()
                
                if atividades_recentes:
                    resposta = f"Atividades recentes de {aluno.nome_completo}:\n\n"
                    
                    for atividade in atividades_recentes:
                        resposta += f"• {atividade.data_realizacao.strftime('%d/%m/%Y')}: {atividade.descricao[:100]}...\n"
                    
                    return {
                        'resposta': resposta,
                        'dados': {
                            'quantidade_atividades': len(atividades_recentes)
                        }
                    }
                else:
                    return {'resposta': f'Não há atividades registradas para {aluno.nome_completo} nos últimos 7 dias.'}
                    
            except Exception as e:
                return {'resposta': 'Erro ao consultar atividades. Tente novamente mais tarde.'}
        else:
            return {
                'resposta': 'Para consultar atividades específicas, preciso saber qual aluno. As atividades são planejadas de acordo com a faixa etária e desenvolvimento pedagógico.',
                'opcoes': ['Tipos de atividades realizadas', 'Cronograma de atividades']
            }
    
    def _resposta_horario(self):
        return {
            'resposta': 'A Escola Infantil UniFAAT-ADS funciona de segunda a sexta-feira, das 7h às 19h. Estamos fechados aos sábados, domingos e feriados.',
            'dados': {
                'horario_funcionamento': '07:00 - 19:00',
                'dias_funcionamento': 'Segunda a Sexta'
            }
        }
    
    def _resposta_contato(self):
        return {
            'resposta': 'Para entrar em contato conosco:\n\n• Telefone: (XX) XXXX-XXXX\n• Email: contato@unifaat-ads.edu.br\n• Endereço: [Endereço da escola]\n• Horário de atendimento: Segunda a Sexta, 7h às 19h\n\nPara assuntos urgentes, procure a secretaria presencialmente.',
            'opcoes': ['Agendar reunião', 'Falar com a direção', 'Secretaria']
        }
    
    def _resposta_padrao(self):
        return {
            'resposta': 'Desculpe, não entendi sua pergunta. Posso ajudá-lo com informações sobre:\n\n• Pagamentos e mensalidades\n• Frequência e presenças\n• Atividades pedagógicas\n• Horário de funcionamento\n• Informações de contato\n\nPor favor, reformule sua pergunta ou escolha uma das opções acima.',
            'opcoes': [
                'Consultar pagamentos',
                'Verificar presenças', 
                'Ver atividades',
                'Horário de funcionamento',
                'Falar com atendente'
            ]
        }

chatbot = ChatBot()

@chatbot_bp.route('/mensagem', methods=['POST'])
def processar_mensagem():
    """
    Processar mensagem do usuário e retornar resposta do chatbot
    ---
    tags:
      - Chatbot
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - mensagem
          properties:
            mensagem:
              type: string
              example: "Quais pagamentos estão pendentes?"
            id_aluno:
              type: integer
              example: 1
    responses:
      200:
        description: Resposta do chatbot
        examples:
          application/json: {
            "mensagem_usuario": "Quais pagamentos estão pendentes?",
            "resposta_bot": "Olá! Encontrei 1 pagamento(s) pendente(s) para Lucas Pereira:\n\n• Maio/2024: R$ 800.00 (Vencimento: 2024-05-10)\n\nTotal devido: R$ 800.00",
            "opcoes": ["Como fazer um pagamento?", "Formas de pagamento aceitas"],
            "dados_adicionais": {"total_pendente": 800.00, "quantidade": 1},
            "timestamp": "2024-06-21T10:00:00"
          }
      400:
        description: Mensagem não fornecida
        examples:
          application/json: {"error": "Mensagem é obrigatória"}
      500:
        description: Erro interno do chatbot
        examples:
          application/json: {"resposta_bot": "Desculpe, ocorreu um erro interno. Tente novamente mais tarde ou entre em contato com a secretaria.", "erro": true}
    """
    data = request.get_json()
    
    if not data or 'mensagem' not in data:
        return jsonify({'error': 'Mensagem é obrigatória'}), 400
    
    mensagem = data['mensagem']
    id_aluno = data.get('id_aluno')
    
    try:
        resposta = chatbot.processar_mensagem(mensagem, id_aluno)
        
        # Log da conversa (opcional - para análise e melhoria)
        # Aqui você poderia salvar a conversa no banco de dados
        
        return jsonify({
            'mensagem_usuario': mensagem,
            'resposta_bot': resposta['resposta'],
            'opcoes': resposta.get('opcoes', []),
            'dados_adicionais': resposta.get('dados', {}),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'resposta_bot': 'Desculpe, ocorreu um erro interno. Tente novamente mais tarde ou entre em contato com a secretaria.',
            'erro': True
        }), 500

@chatbot_bp.route('/opcoes', methods=['GET'])
def get_opcoes_iniciais():
    """
    Obter opções iniciais do chatbot
    ---
    tags:
      - Chatbot
    responses:
      200:
        description: Opções iniciais e mensagem de boas-vindas
        examples:
          application/json: {
            "mensagem_boas_vindas": "Olá! Sou o assistente virtual da Escola Infantil UniFAAT-ADS. Como posso ajudá-lo?",
            "opcoes_principais": [
              "Consultar pagamentos",
              "Verificar presenças",
              "Ver atividades",
              "Horário de funcionamento",
              "Informações de contato"
            ],
            "disponibilidade": "24 horas por dia, 7 dias por semana"
          }
    """
    return jsonify({
        'mensagem_boas_vindas': 'Olá! Sou o assistente virtual da Escola Infantil UniFAAT-ADS. Como posso ajudá-lo?',
        'opcoes_principais': [
            'Consultar pagamentos',
            'Verificar presenças',
            'Ver atividades',
            'Horário de funcionamento',
            'Informações de contato'
        ],
        'disponibilidade': '24 horas por dia, 7 dias por semana'
    })

@chatbot_bp.route('/transferir', methods=['POST'])
def transferir_atendimento():
    """
    Transferir atendimento para contato humano
    ---
    tags:
      - Chatbot
    parameters:
      - in: body
        name: body
        required: false
        schema:
          type: object
          properties:
            nome:
              type: string
              example: "Maria Oliveira"
            email:
              type: string
              example: "maria.oliveira@email.com"
            telefone:
              type: string
              example: "(11) 91234-5678"
            assunto:
              type: string
              example: "Dúvida sobre pagamento"
            mensagem:
              type: string
              example: "Gostaria de saber sobre descontos."
    responses:
      200:
        description: Contato da secretaria e formulário de contato
        examples:
          application/json: {
            "mensagem": "Entendi que você precisa de atendimento personalizado. Por favor, entre em contato com nossa secretaria:",
            "contatos": {
              "telefone": "(11) 91234-5678",
              "email": "contato@unifaat-ads.edu.br",
              "horario_atendimento": "Segunda a Sexta, 7h às 19h"
            },
            "formulario_contato": {
              "disponivel": true,
              "campos": ["nome", "email", "telefone", "assunto", "mensagem"]
            }
          }
    """
    data = request.get_json()
    
    return jsonify({
        'mensagem': 'Entendi que você precisa de atendimento personalizado. Por favor, entre em contato com nossa secretaria:',
        'contatos': {
            'telefone': '(XX) XXXX-XXXX',
            'email': 'contato@unifaat-ads.edu.br',
            'horario_atendimento': 'Segunda a Sexta, 7h às 19h'
        },
        'formulario_contato': {
            'disponivel': True,
            'campos': ['nome', 'email', 'telefone', 'assunto', 'mensagem']
        }
    })