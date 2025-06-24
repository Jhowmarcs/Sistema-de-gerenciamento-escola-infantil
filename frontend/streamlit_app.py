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
    nivel = st.session_state.usuario_info['nivel_acesso'].strip().lower()
    st.sidebar.write(f"**Nível (debug):** {nivel}")
    if nivel == 'administrador':
        opcoes.insert(1, "Usuários")
    opcoes.append("Meu Perfil")
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
                st.write("### Lista de Pagamentos")
                for pagamento in pagamentos:
                    col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,2,1,1])
                    col1.write(f"ID: {pagamento['id_pagamento']}")
                    col2.write(f"Aluno: {pagamento['id_aluno']}")
                    col3.write(f"Valor: R$ {pagamento['valor_pago']:.2f}")
                    col4.write(f"Status: {pagamento['status']}")
                    editar = col5.button("Editar", key=f"edit_pag_{pagamento['id_pagamento']}")
                    excluir = col6.button("Excluir", key=f"del_pag_{pagamento['id_pagamento']}")
                    if editar:
                        with st.form(f"form_edit_pag_{pagamento['id_pagamento']}"):
                            novo_valor = st.number_input("Valor Pago", value=pagamento['valor_pago'], format="%.2f")
                            nova_referencia = st.text_input("Referência", value=pagamento['referencia'])
                            novo_status = st.selectbox("Status", ["Pago", "Pendente"], index=0 if pagamento['status']=="Pago" else 1)
                            submit_edit = st.form_submit_button("Salvar Alterações")
                            if submit_edit:
                                data = {
                                    "valor_pago": novo_valor,
                                    "referencia": nova_referencia,
                                    "status": novo_status
                                }
                                resultado = fazer_requisicao(f"/api/pagamentos/{pagamento['id_pagamento']}", "PUT", data)
                                if resultado:
                                    st.success("Pagamento atualizado com sucesso!")
                                    st.rerun()
                    if excluir:
                        if st.confirm(f"Tem certeza que deseja excluir o pagamento {pagamento['id_pagamento']}?"):
                            resultado = fazer_requisicao(f"/api/pagamentos/{pagamento['id_pagamento']}", "DELETE")
                            if resultado:
                                st.success("Pagamento excluído com sucesso!")
                                st.rerun()
            else:
                st.info("Nenhum pagamento registrado.")
        
        with tab2:
            alunos = fazer_requisicao("/api/alunos")
            
            with st.form("registro_pagamento"):
                if alunos:
                    aluno_opcoes = {a['id_aluno]: a['nome_completo'] for a in alunos}
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
    
    # Gerenciamento de Presenças
    elif opcao_selecionada == "Presenças":
        st.title("🗓️ Gerenciamento de Presenças")
        tab1, tab2, tab3 = st.tabs(["Lista de Presenças", "Registrar Presença", "Relatório de Frequência"])

        with tab1:
            st.subheader("Consultar Presenças por Data")
            data_presenca = st.date_input("Selecione a data", value=date.today())
            if st.button("Buscar Presenças"):
                presencas = fazer_requisicao(f"/api/presencas/data/{data_presenca}")
                if presencas:
                    df = pd.DataFrame(presencas)
                    st.dataframe(df, use_container_width=True)
                    # Adiciona opções de editar/excluir
                    for idx, row in df.iterrows():
                        col1, col2 = st.columns([1,1])
                        with col1:
                            if st.button(f"Editar", key=f"edit_pres_{row['id_presenca']}"):
                                with st.form(f"form_edit_pres_{row['id_presenca']}"):
                                    novo_presente = st.selectbox("Presente?", [True, False], index=0 if row['presente'] else 1)
                                    submit_edit = st.form_submit_button("Salvar Alterações")
                                    if submit_edit:
                                        data = {"presente": novo_presente}
                                        resultado = fazer_requisicao(f"/api/presencas/{row['id_presenca']}", "PUT", data)
                                        if resultado:
                                            st.success("Presença atualizada com sucesso!")
                                            st.rerun()
                        with col2:
                            if st.button(f"Excluir", key=f"del_pres_{row['id_presenca']}"):
                                if st.confirm(f"Tem certeza que deseja excluir a presença {row['id_presenca']}?"):
                                    resultado = fazer_requisicao(f"/api/presencas/{row['id_presenca']}", "DELETE")
                                    if resultado:
                                        st.success("Presença excluída com sucesso!")
                                        st.rerun()
                else:
                    st.info("Nenhuma presença registrada para esta data.")

        with tab2:
            st.subheader("Registrar Presença de Aluno")
            alunos = fazer_requisicao("/api/alunos")
            if alunos:
                aluno_opcoes = {a['id_aluno']: a['nome_completo'] for a in alunos}
                id_aluno = st.selectbox("Aluno", options=list(aluno_opcoes.keys()), format_func=lambda x: aluno_opcoes[x])
                data_presenca = st.date_input("Data da Presença", value=date.today(), key="data_presenca_registro")
                presente = st.selectbox("Presença", ["Presente", "Faltou"])
                if st.button("Registrar Presença"):
                    data = {
                        "id_aluno": id_aluno,
                        "data": data_presenca.strftime("%Y-%m-%d"),
                        "presente": presente == "Presente"
                    }
                    resultado = fazer_requisicao("/api/presencas", "POST", data)
                    if resultado:
                        st.success("Presença registrada com sucesso!")
                        st.rerun()
            else:
                st.info("Nenhum aluno cadastrado.")

        with tab3:
            st.subheader("Relatório de Frequência por Aluno")
            alunos = fazer_requisicao("/api/alunos")
            if alunos:
                aluno_opcoes = {a['id_aluno']: a['nome_completo'] for a in alunos}
                id_aluno = st.selectbox("Selecione o aluno", options=list(aluno_opcoes.keys()), format_func=lambda x: aluno_opcoes[x], key="aluno_freq")
                if st.button("Gerar Relatório de Frequência"):
                    relatorio = fazer_requisicao(f"/api/presencas/aluno/{id_aluno}")
                    if relatorio:
                        df = pd.DataFrame(relatorio)
                        st.dataframe(df, use_container_width=True)
                        total_presencas = sum(1 for p in relatorio if p.get('presente'))
                        st.metric("Total de Presenças", total_presencas)
                    else:
                        st.info("Nenhuma presença registrada para este aluno.")
            else:
                st.info("Nenhum aluno cadastrado.")
    
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
            st.session_state.chat_history.append({
                'tipo': 'usuario',
                'conteudo': prompt
            })
            st.chat_message("user").write(prompt)
            data = {"mensagem": prompt}
            resposta = fazer_requisicao("/api/chatbot/mensagem", "POST", data)
            if resposta and 'resposta_bot' in resposta:
                bot_response = resposta['resposta_bot']
                st.session_state.chat_history.append({
                    'tipo': 'bot',
                    'conteudo': bot_response
                })
                st.chat_message("assistant").write(bot_response)
                if 'opcoes' in resposta and resposta['opcoes']:
                    st.write("**Opções disponíveis:**")
                    for opcao in resposta['opcoes']:
                        if st.button(opcao, key=f"opcao_{len(st.session_state.chat_history)}_{opcao}"):
                            data_opcao = {"mensagem": opcao}
                            resposta_opcao = fazer_requisicao("/api/chatbot/mensagem", "POST", data_opcao)
                            if resposta_opcao and 'resposta_bot' in resposta_opcao:
                                st.session_state.chat_history.append({
                                    'tipo': 'usuario',
                                    'conteudo': opcao
                                })
                                st.session_state.chat_history.append({
                                    'tipo': 'bot',
                                    'conteudo': resposta_opcao['resposta_bot']
                                })
                                st.rerun()
                            else:
                                st.error("Erro ao obter resposta do ChatBot para a opção selecionada.")
            else:
                st.session_state.chat_history.append({
                    'tipo': 'bot',
                    'conteudo': 'Desculpe, não foi possível obter resposta do ChatBot.'
                })
                st.chat_message("assistant").write('Desculpe, não foi possível obter resposta do ChatBot.')
        if st.button("Limpar Conversa"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Gerenciamento de Atividades
    elif opcao_selecionada == "Atividades":
        st.title("🎨 Gerenciamento de Atividades")
        tab1, tab2, tab3 = st.tabs(["Lista de Atividades", "Cadastrar Atividade", "Relatório de Atividades"])

        with tab1:
            st.write("### Lista de Atividades")
            atividades = fazer_requisicao("/api/atividades")
            if atividades:
                for atividade in atividades:
                    col1, col2, col3, col4 = st.columns([2,2,1,1])
                    col1.write(f"ID: {atividade['id_atividade']}")
                    col2.write(f"Descrição: {atividade['descricao']}")
                    editar = col3.button("Editar", key=f"edit_ativ_{atividade['id_atividade']}")
                    excluir = col4.button("Excluir", key=f"del_ativ_{atividade['id_atividade']}")
                    if editar:
                        with st.form(f"form_edit_ativ_{atividade['id_atividade']}"):
                            nova_desc = st.text_input("Descrição", value=atividade['descricao'])
                            nova_data = st.date_input("Data", value=datetime.strptime(atividade['data_realizacao'], "%Y-%m-%d"))
                            submit_edit = st.form_submit_button("Salvar Alterações")
                            if submit_edit:
                                data = {
                                    "descricao": nova_desc,
                                    "data_realizacao": nova_data.strftime("%Y-%m-%d")
                                }
                                resultado = fazer_requisicao(f"/api/atividades/{atividade['id_atividade']}", "PUT", data)
                                if resultado:
                                    st.success("Atividade atualizada com sucesso!")
                                    st.rerun()
                    if excluir:
                        if st.confirm(f"Tem certeza que deseja excluir a atividade {atividade['id_atividade']}?"):
                            resultado = fazer_requisicao(f"/api/atividades/{atividade['id_atividade']}", "DELETE")
                            if resultado:
                                st.success("Atividade excluída com sucesso!")
                                st.rerun()
            else:
                st.info("Nenhuma atividade cadastrada.")

        with tab2:
            turmas = fazer_requisicao("/api/turmas")
            if turmas:
                turma_opcoes = {t['id_turma']: t['nome_turma'] for t in turmas}
                with st.form("cadastro_atividade"):
                    nome = st.text_input("Nome da Atividade")
                    descricao = st.text_area("Descrição")
                    id_turma = st.selectbox("Turma", options=list(turma_opcoes.keys()), format_func=lambda x: turma_opcoes[x])
                    data_atividade = st.date_input("Data da Atividade", value=date.today(), key="data_atividade")
                    submit = st.form_submit_button("Cadastrar")
                    if submit:
                        data = {
                            "nome": nome,
                            "descricao": descricao,
                            "id_turma": id_turma,
                            "data": data_atividade.strftime("%Y-%m-%d")
                        }
                        resultado = fazer_requisicao("/api/atividades", "POST", data)
                        if resultado:
                            st.success("Atividade cadastrada com sucesso!")
                            st.rerun()
            else:
                st.info("Nenhuma turma cadastrada.")

        with tab3:
            st.subheader("Relatório de Atividades por Turma")
            turmas = fazer_requisicao("/api/turmas")
            if turmas:
                turma_opcoes = {t['id_turma']: t['nome_turma'] for t in turmas}
                id_turma = st.selectbox("Selecione a turma", options=list(turma_opcoes.keys()), format_func=lambda x: turma_opcoes[x], key="turma_ativ")
                if st.button("Gerar Relatório de Atividades"):
                    relatorio = fazer_requisicao(f"/api/atividades?turma={id_turma}")
                    if relatorio:
                        df = pd.DataFrame(relatorio)
                        st.dataframe(df, use_container_width=True)
                        st.metric("Total de Atividades", len(relatorio))
                    else:
                        st.info("Nenhuma atividade registrada para esta turma.")
            else:
                st.info("Nenhuma turma cadastrada.")
    
    # Relatórios Gerais
    elif opcao_selecionada == "Relatórios":
        st.title("📑 Relatórios do Sistema")
        tab1, tab2, tab3, tab4 = st.tabs([
            "Pagamentos por Período",
            "Inadimplência",
            "Frequência Geral",
            "Atividades por Turma"
        ])

        with tab1:
            st.subheader("Relatório de Pagamentos por Período")
            data_ini = st.date_input("Data Inicial", value=date.today(), key="data_ini_pag")
            data_fim = st.date_input("Data Final", value=date.today(), key="data_fim_pag")
            if st.button("Gerar Relatório de Pagamentos"):
                relatorio = fazer_requisicao(f"/api/pagamentos/relatorio/periodo?data_ini={data_ini}&data_fim={data_fim}")
                if relatorio:
                    df = pd.DataFrame(relatorio)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhum pagamento encontrado no período.")

        with tab2:
            st.subheader("Relatório de Inadimplência")
            if st.button("Gerar Relatório de Inadimplência", key="btn_inad"):
                relatorio = fazer_requisicao("/api/pagamentos/relatorio/inadimplencia")
                if relatorio:
                    st.metric("Total de Inadimplentes", relatorio['total_inadimplentes'])
                    st.metric("Valor Total Devido", f"R$ {relatorio['valor_total_devido']:.2f}")
                    if relatorio['inadimplentes']:
                        df = pd.DataFrame(relatorio['inadimplentes'])
                        st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhum inadimplente encontrado.")

        with tab3:
            st.subheader("Relatório de Frequência Geral")
            if st.button("Gerar Relatório de Frequência Geral"):
                relatorio = fazer_requisicao("/api/presencas/relatorio/frequencia")
                if relatorio:
                    df = pd.DataFrame(relatorio)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Nenhuma frequência registrada.")

        with tab4:
            st.subheader("Relatório de Atividades por Turma")
            turmas = fazer_requisicao("/api/turmas")
            if turmas:
                turma_opcoes = {t['id_turma']: t['nome_turma'] for t in turmas}
                id_turma = st.selectbox("Selecione a turma", options=list(turma_opcoes.keys()), format_func=lambda x: turma_opcoes[x], key="turma_relatorio_ativ")
                if st.button("Gerar Relatório de Atividades", key="btn_ativ_rel"):
                    relatorio = fazer_requisicao(f"/api/atividades?turma={id_turma}")
                    if relatorio:
                        df = pd.DataFrame(relatorio)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("Nenhuma atividade registrada para esta turma.")
            else:
                st.info("Nenhuma turma cadastrada.")
    
    # Cadastro de Usuários (apenas admin)
    elif opcao_selecionada == "Usuários":
        st.title("👤 Cadastro de Usuários")
        with st.form("cadastro_usuario"):
            login = st.text_input("Login")
            senha = st.text_input("Senha", type="password")
            nivel = st.selectbox("Nível de Acesso", ["Administrador", "Secretaria", "Professor"])
            submit = st.form_submit_button("Cadastrar Usuário")
            if submit:
                data = {"login": login, "senha": senha, "nivel_acesso": nivel}
                resultado = fazer_requisicao("/api/auth/register", "POST", data)
                if resultado:
                    st.success("Usuário cadastrado com sucesso!")
                else:
                    st.error("Erro ao cadastrar usuário.")
    
    # Edição de perfil do usuário logado
    elif opcao_selecionada == "Meu Perfil":
        st.title("👤 Meu Perfil")
        usuario = st.session_state.usuario_info
        with st.form("editar_perfil"):
            login = st.text_input("Login", value=usuario['login'], disabled=True)
            senha = st.text_input("Nova Senha", type="password")
            # Permite editar apenas o próprio perfil, exceto login e nível
            if usuario['nivel_acesso'] == 'Professor':
                nome = st.text_input("Nome Completo", value=usuario.get('nome_completo', ''))
                email = st.text_input("Email", value=usuario.get('email', ''))
            else:
                nome = st.text_input("Nome Completo", value=usuario.get('nome_completo', ''), disabled=True)
                email = st.text_input("Email", value=usuario.get('email', ''), disabled=True)
            submit = st.form_submit_button("Salvar Alterações")
            if submit:
                data = {}
                if senha:
                    data['senha'] = senha
                if usuario['nivel_acesso'] == 'Professor':
                    data['nome_completo'] = nome
                    data['email'] = email
                if data:
                    resultado = fazer_requisicao(f"/api/auth/update/{usuario['login']}", "PUT", data)
                    if resultado:
                        st.success("Perfil atualizado com sucesso!")
                        st.session_state.usuario_info.update(data)
                    else:
                        st.error("Erro ao atualizar perfil.")
                else:
                    st.info("Nenhuma alteração realizada.")
    
    # Outras seções podem ser implementadas de forma similar...
    else:
        st.title(f"🚧 {opcao_selecionada}")
        st.info("Esta seção está em desenvolvimento.")