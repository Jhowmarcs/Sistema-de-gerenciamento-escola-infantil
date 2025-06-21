from app import create_app, db
from app.models import Usuario, Professor, Turma, Aluno, Pagamento, Presenca, Atividade, AtividadeAluno
import time
import os

app = create_app()

@app.route('/')
def index():
    return {
        'message': 'Sistema de Gerenciamento Escolar Infantil - API',
        'version': '1.0',
        'status': 'ativo',
        'endpoints': {
            'auth': '/api/auth',
            'alunos': '/api/alunos',
            'professores': '/api/professores',
            'turmas': '/api/turmas',
            'pagamentos': '/api/pagamentos',
            'presencas': '/api/presencas',
            'atividades': '/api/atividades',
            'chatbot': '/api/chatbot'
        }
    }

@app.route('/health')
def health_check():
    return {'status': 'healthy', 'database': 'connected'}

def wait_for_db():
    """Aguarda o banco de dados estar disponível"""
    import psycopg2
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Tenta conectar no banco
            db_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/escola_infantil')
            # Parse da URL para extrair componentes
            if 'postgresql://' in db_url:
                parts = db_url.replace('postgresql://', '').split('@')
                user_pass = parts[0].split(':')
                host_db = parts[1].split('/')
                host_port = host_db[0].split(':')
                
                conn = psycopg2.connect(
                    host=host_port[0],
                    port=int(host_port[1]) if len(host_port) > 1 else 5432,
                    database=host_db[1],
                    user=user_pass[0],
                    password=user_pass[1]
                )
                conn.close()
                print("✅ Banco de dados conectado com sucesso!")
                return True
        except Exception as e:
            retry_count += 1
            print(f"⏳ Aguardando banco de dados... Tentativa {retry_count}/{max_retries}")
            time.sleep(2)
    
    print("❌ Não foi possível conectar ao banco de dados")
    return False

if __name__ == '__main__':
    # Aguarda o banco estar disponível
    if wait_for_db():
        with app.app_context():
            try:
                db.create_all()
                print("✅ Tabelas criadas com sucesso!")
                
                # Criar usuário administrador padrão se não existir
                admin = Usuario.query.filter_by(login='admin').first()
                if not admin:
                    admin_user = Usuario(
                        login='admin',
                        senha='admin123',
                        nivel_acesso='administrador'
                    )
                    db.session.add(admin_user)
                    db.session.commit()
                    print("✅ Usuário administrador criado: admin/admin123")
                
            except Exception as e:
                print(f"❌ Erro ao inicializar banco: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)