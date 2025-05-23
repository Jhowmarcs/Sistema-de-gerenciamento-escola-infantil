from app import create_app, db

app = create_app()

# Cria as tabelas, se não existirem
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
