import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date
import os

# Configuração da página
st.set_page_config(
    page_title="Sistema Escolar Infantil",
    page_icon="🏫",
    layout="wide"
)

# URL da API
API_URL = os.environ.get('API_URL', 'http://localhost:5000')

# Funções auxiliares
def fazer_requisicao(endpoint, method='GET', data=None):
    """Função para fazer requisições à API"""
    try:
        url = f"{API_URL}{endpoint}"
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, json=data)
        elif method == 'PUT':
            response = requests.put(url, json=data)
        elif method == 'DELETE':
            response = requests.delete(url)
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            st.error(f"Erro na requisição: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro de conexão: {str(e)}")
        return None

# Sidebar para navegação
st.sidebar.title("🏫 Sistema Escolar")
st.sidebar.markdown("---")

# Verificar se o usuário está logado
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = False

if not st.session_state.usuario_logado:
    # Página de Login
    st.title("Login - Sistema Escolar Infantil")
    
    with st.form("login_form"):
        login = st.text_input("Login")
        senha = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            data = {"login": login, "senha": senha}
            resultado = fazer_requisicao("/api/auth/login", "POST", data)
            
            if resultado:
                st.session_state.usuario_logado = True
                st.session_state.usuario_info = resultado['usuario']
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas!")

else:
    # Menu principal
    opcoes = [
        "Dashboard",
        "Alunos", 
        "Professores",
        "Turmas",
        "Pagamentos",
        "Presenças", 
        "Atividades",
        "ChatBot",
        "Relatórios"
    ]
    
    opcao_selecionada = st.sidebar.selectbox("Selecione uma opção:", opcoes)
    
    # Botão de logout
    if st.sidebar.button("Logout"):
        st.session_state.usuario_logado = False
        st.session_state.usuario_info = None
        st.rerun()
    
    # Mostrar informações do usuário
    st.sidebar.markdown("---")
    st.sidebar.write(f"**Usuário:** {st.session_state.usuario_info['login']}")
    st.sidebar.write(f"**Nível:** {st.session_state.usuario_info['nivel_acesso']}")
    
    # Dashboard
    if opcao_selecionada == "Dashboard":
        st.title("📊 Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Estatísticas gerais
        alunos = fazer_requisicao("/api/alunos")
        professores = fazer_requisicao("/api/professores")
        turmas = fazer_requisicao("/api/turmas")
        
        with col1:
            st.metric("Total de Alunos", len(alunos) if alunos else 0)
        
        with col2:
            st.metric("Total de Professores", len(professores) if professores else 0)
        
        with col3:
            st.metric("Total de Turmas", len(turmas) if turmas else 0)
        
        with col4:
            # Pagamentos pendentes
            pagamentos = fazer_requisicao("/api/pagamentos")
            pendentes = len([p for p in pagamentos if p['status'] == 'Pendente']) if pagamentos else 0
            st.metric("Pagamentos Pendentes", pendentes)
    
    # Gerenciamento de Alunos
    elif opcao_selecionada == "Alunos":
        st.title("👶 Gerenciamento de Alunos")
        
        tab1, tab2 = st.tabs(["Lista de Alunos", "Cadastrar Aluno"])
        
        with tab1:
            st.subheader("Lista de Alunos")
            alunos = fazer_requisicao("/api/alunos")
            
            if alunos:
                df = pd.DataFrame(alunos)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum aluno cadastrado.")
        
        with tab2:
            st.subheader("Cadastrar Novo Aluno")
            
            # Buscar turmas para o select
            turmas = fazer_requisicao("/api/turmas")
            
            with st.form("cadastro_aluno"):
                nome = st.text_input("Nome Completo")
                data_nasc = st.date_input("Data de Nascimento")
                
                if turmas:
                    turma_opcoes = {t['id_turma']: t['nome_turma'] for t in turmas}
                    id_turma = st.selectbox("Turma", options=list(turma_opcoes.keys()), 
                                          format_func=lambda x: turma_opcoes[x])
                else:
                    st.warning("Nenhuma turma cadastrada!")
                    id_turma = None
                
                nome_resp = st.text_input("Nome do Responsável")
                tel_resp = st.text_input("Telefone do Responsável")
                email_resp = st.text_input("Email do Responsável")
                info_add = st.text_area("Informações Adicionais")
                
                submit = st.form_submit_button("Cadastrar")
                
                if submit and id_turma:
                    data = {
                        "nome_completo": nome,
                        "data_nascimento": data_nasc.strftime("%Y-%m-%d"),
                        "id_turma": id_turma,
                        "nome_responsavel": nome_resp,
                        "telefone_responsavel": tel_resp,
                        "email_responsavel": email_resp,
                        "informacoes_adicionais": info_add
                    }
                    
                    resultado = fazer_requisicao("/api/alunos", "POST", data)
                    if resultado:
                        st.success("Aluno cadastrado com sucesso!")
                        st.rerun()
    
    # Gerenciamento de Professores
    elif opcao_selecionada == "Professores":
        st.title("👨‍🏫 Gerenciamento de Professores")
        
        tab1, tab2 = st.tabs(["Lista de Professores", "Cadastrar Professor"])
        
        with tab1:
            professores = fazer_requisicao("/api/professores")
            if professores:
                df = pd.DataFrame(professores)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum professor cadastrado.")
        
        with tab2:
            with st.form("cadastro_professor"):
                nome = st.text_input("Nome Completo")
                email = st.text_input("Email")
                telefone = st.text_input("Telefone")
                
                submit = st.form_submit_button("Cadastrar")
                
                if submit:
                    data = {
                        "nome_completo": nome,
                        "email": email,
                        "telefone": telefone
                    }
                    
                    resultado = fazer_requisicao("/api/professores", "POST", data)
                    if resultado:
                        st.success("Professor cadastrado com sucesso!")
                        st.rerun()
    
    # Gerenciamento de Turmas
    elif opcao_selecionada == "Turmas":
        st.title("🏛️ Gerenciamento de Turmas")
        
        tab1, tab2 = st.tabs(["Lista de Turmas", "Cadastrar Turma"])
        
        with tab1:
            turmas = fazer_requisicao("/api/turmas")
            if turmas:
                df = pd.DataFrame(turmas)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhuma turma cadastrada.")
        
        with tab2:
            professores = fazer_requisicao("/api/professores")
            
            with st.form("cadastro_turma"):
                nome_turma = st.text_input("Nome da Turma")
                
                if professores:
                    prof_opcoes = {p['id_professor']: p['nome_completo'] for p in professores}
                    id_professor = st.selectbox("Professor Responsável", 
                                              options=list(prof_opcoes.keys()),
                                              format_func=lambda x: prof_opcoes[x])
                else:
                    st.warning("Nenhum professor cadastrado!")
                    id_professor = None
                
                horario = st.text_input("Horário")
                
                submit = st.form_submit_button("Cadastrar")
                
                if submit and id_professor:
                    data = {
                        "nome_turma": nome_turma,
                        "id_professor": id_professor,
                        "horario": horario
                    }
                    
                    resultado = fazer_requisicao("/api/turmas", "POST", data)
                    if resultado:
                        st.success("Turma cadastrada com sucesso!")
                        st.rerun()
    
    # Gerenciamento de Pagamentos
    elif opcao_selecionada == "Pagamentos":
        st.title("💰 Gerenciamento de Pagamentos")
        
        tab1, tab2, tab3 = st.tabs(["Lista de Pagamentos", "Registrar Pagamento", "Relatórios"])
        
        with tab1:
            pagamentos = fazer_requisicao("/api/pagamentos")
            if pagamentos:
                df = pd.DataFrame(pagamentos)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Nenhum pagamento registrado.")
        
        with tab2:
            alunos = fazer_requisicao("/api/alunos")
            
            with st.form("registro_pagamento"):
                if alunos:
                    aluno_opcoes = {a['id_aluno']: a['nome_completo'] for a in alunos}
                    id_aluno = st.selectbox("Aluno", options=list(aluno_opcoes.keys()),
                                          format_func=lambda x: aluno_opcoes[x])
                else:
                    st.warning("Nenhum aluno cadastrado!")
                    id_aluno = None
                
                data_pag = st.date_input("Data do Pagamento")
                valor = st.number_input("Valor Pago", min_value=0.0, format="%.2f")
                forma = st.selectbox("Forma de Pagamento", 
                                   ["Dinheiro", "PIX", "Cartão de Crédito", "Cartão de Débito"])
                referencia = st.text_input("Referência (ex: Mensalidade Janeiro/2024)")
                status = st.selectbox("Status", ["Pago", "Pendente"])
                
                submit = st.form_submit_button("Registrar")
                
                if submit and id_aluno:
                    data = {
                        "id_aluno": id_aluno,
                        "data_pagamento": data_pag.strftime("%Y-%m-%d"),
                        "valor_pago": valor,
                        "forma_pagamento": forma,
                        "referencia": referencia,
                        "status": status
                    }
                    
                    resultado = fazer_requisicao("/api/pagamentos", "POST", data)
                    if resultado:
                        st.success("Pagamento registrado com sucesso!")
                        st.rerun()
        
        with tab3:
            st.subheader("Relatório de Inadimplência")
            if st.button("Gerar Relatório"):
                relatorio = fazer_requisicao("/api/pagamentos/relatorio/inadimplencia")
                if relatorio:
                    st.metric("Total de Inadimplentes", relatorio['total_inadimplentes'])
                    st.metric("Valor Total Devido", f"R$ {relatorio['valor_total_devido']:.2f}")
                    
                    if relatorio['inadimplentes']:
                        df_inad = pd.DataFrame(relatorio['inadimplentes'])
                        st.dataframe(df_inad, use_container_width=True)
    
    # ChatBot
    elif opcao_selecionada == "ChatBot":
        st.title("🤖 ChatBot - Assistente Virtual")
        
        # Inicializar histórico de chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Mostrar histórico
        for msg in st.session_state.chat_history:
            if msg['tipo'] == 'usuario':
                st.chat_message("user").write(msg['conteudo'])
            else:
                st.chat_message("assistant").write(msg['conteudo'])
        
        # Input para nova mensagem
        if prompt := st.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário
            st.session_state.chat_history.append({
                'tipo': 'usuario',
                'conteudo': prompt
            })
            st.chat_message("user").write(prompt)
            
            # Enviar para o ChatBot
            data = {"mensagem": prompt}
            resposta = fazer_requisicao("/api/chatbot/mensagem", "POST", data)
            
            if resposta:
                bot_response = resposta['resposta_bot']
                st.session_state.chat_history.append({
                    'tipo': 'bot',
                    'conteudo': bot_response
                })
                st.chat_message("assistant").write(bot_response)
                
                # Mostrar opções se disponíveis
                if 'opcoes' in resposta and resposta['opcoes']:
                    st.write("**Opções disponíveis:**")
                    for opcao in resposta['opcoes']:
                        if st.button(opcao, key=f"opcao_{len(st.session_state.chat_history)}_{opcao}"):
                            # Processar opção selecionada
                            data_opcao = {"mensagem": opcao}
                            resposta_opcao = fazer_requisicao("/api/chatbot/mensagem", "POST", data_opcao)
                            if resposta_opcao:
                                st.session_state.chat_history.append({
                                    'tipo': 'usuario',
                                    'conteudo': opcao
                                })
                                st.session_state.chat_history.append({
                                    'tipo': 'bot',
                                    'conteudo': resposta_opcao['resposta_bot']
                                })
                                st.rerun()
        
        # Botão para limpar chat
        if st.button("Limpar Conversa"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Outras seções podem ser implementadas de forma similar...
    else:
        st.title(f"🚧 {opcao_selecionada}")
        st.info("Esta seção está em desenvolvimento.")