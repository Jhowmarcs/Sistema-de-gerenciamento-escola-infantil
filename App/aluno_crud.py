import os
import psycopg2
import logging
from logging.handlers import RotatingFileHandler
from psycopg2 import Error

# Configuração do logger com rotação de logs
logger = logging.getLogger("escola_infantil")
logger.setLevel(logging.DEBUG)

# O arquivo de log será colocado em /app/escola_infantil.log dentro do container,
# e com o volume mapeado você poderá acessar no host.
handler = RotatingFileHandler("/app/escola_infantil.log", maxBytes=1048576, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Teste: o arquivo de log foi iniciado em aluno_crud.py")

def get_connection():
    """
    Cria e retorna uma conexão com o banco de dados PostgreSQL utilizando a variável de ambiente DATABASE_URL.
    """
    try:
        # Lê a string de conexão a partir da variável de ambiente
        database_url = os.getenv("DATABASE_URL", "postgresql://postgres:secret@db:5432/nome_banco")
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        logger.error(f"ERRO: Falha na conexão com o banco de dados - {e}")
        raise

def create_aluno(nome, idade, turma):
    """
    Insere um novo aluno no banco de dados.
    Retorna o ID gerado ou None se a operação falhar.
    """
    conn = None
    aluno_id = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "INSERT INTO alunos (nome, idade, turma) VALUES (%s, %s, %s) RETURNING id"
        cur.execute(query, (nome, idade, turma))
        aluno_id = cur.fetchone()[0]
        conn.commit()
        logger.info(f"CREATE: Aluno {{'nome': '{nome}', 'idade': {idade}, 'turma': '{turma}'}} inserido com sucesso. ID gerado: {aluno_id}")
        cur.close()
    except psycopg2.Error as e:
        logger.error(f"CREATE: Erro ao inserir novo aluno - {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    return aluno_id

def get_alunos():
    """
    Retorna uma lista de todos os alunos presentes no banco de dados.
    """
    conn = None
    alunos = []
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "SELECT id, nome, idade, turma FROM alunos"
        cur.execute(query)
        alunos = cur.fetchall()
        logger.info("READ: Listagem de todos os alunos solicitada.")
        cur.close()
    except psycopg2.Error as e:
        logger.error(f"READ: Erro ao listar alunos - {e}")
    finally:
        if conn:
            conn.close()
    return alunos

def update_aluno(aluno_id, nome=None, idade=None, turma=None):
    """
    Atualiza os dados de um aluno específico.
    Apenas os campos fornecidos (não nulos) serão atualizados.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        campos = []
        valores = []
        if nome is not None:
            campos.append("nome = %s")
            valores.append(nome)
        if idade is not None:
            campos.append("idade = %s")
            valores.append(idade)
        if turma is not None:
            campos.append("turma = %s")
            valores.append(turma)
        if not campos:
            logger.warning("UPDATE: Nenhum campo fornecido para atualização.")
            return
        query = f"UPDATE alunos SET {', '.join(campos)} WHERE id = %s"
        valores.append(aluno_id)
        cur.execute(query, tuple(valores))
        if cur.rowcount == 0:
            logger.error(f"UPDATE: Aluno com ID {aluno_id} não encontrado para atualização.")
        else:
            conn.commit()
            logger.info(f"UPDATE: Aluno com ID {aluno_id} atualizado com os valores: {{'nome': {nome}, 'idade': {idade}, 'turma': {turma}}}")
        cur.close()
    except psycopg2.Error as e:
        logger.error(f"UPDATE: Erro ao atualizar aluno com ID {aluno_id} - {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def delete_aluno(aluno_id):
    """
    Remove um aluno do banco de dados.
    Verifica se o aluno existe antes de tentar deletar.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM alunos WHERE id = %s", (aluno_id,))
        if cur.fetchone() is None:
            logger.error(f"DELETE: Falha ao deletar aluno com ID {aluno_id} - Aluno não encontrado.")
            return
        query = "DELETE FROM alunos WHERE id = %s"
        cur.execute(query, (aluno_id,))
        conn.commit()
        logger.info(f"DELETE: Aluno com ID {aluno_id} removido com sucesso.")
        cur.close()
    except psycopg2.Error as e:
        logger.error(f"DELETE: Erro ao deletar aluno com ID {aluno_id} - {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

# Bloco para testar as operações CRUD
if __name__ == "__main__":
    novo_id = create_aluno("Carla", 6, "C")
    print("ID do novo aluno:", novo_id)
    
    alunos = get_alunos()
    print("Alunos:", alunos)
    
    # Para testar update e delete, descomente as linhas abaixo:
    # update_aluno(novo_id, nome="Carla Mendes", idade=7)
    # delete_aluno(novo_id)
