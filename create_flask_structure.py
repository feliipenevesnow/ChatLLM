import os

# Estrutura de diretórios
folders = [
    'app',
    'app/templates',
    'app/static/css',
    'app/static/js',
    'app/services'
]

# Arquivos a serem criados e seu conteúdo
files = {
    'app/__init__.py': '''from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
''',

    'app/routes.py': '''from flask import Blueprint, request, jsonify
import openai
from .services.db_service import fetch_insemination_data
from .services.chat_service import ask_chatgpt

bp = Blueprint('main', __name__)

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')

    db_info = fetch_insemination_data()

    full_question = f"Com base nos seguintes dados do banco de inseminação:\\n{db_info}\\n\\n{question}"

    response = ask_chatgpt(full_question)

    return jsonify({'response': response})
''',

    'app/models.py': '''from flask_mysqldb import MySQL

# Este arquivo pode ser utilizado para definir os modelos do banco de dados se você decidir usar SQLAlchemy
''',

    'app/services/chat_service.py': '''import openai

# Configurar a chave da API do ChatGPT
openai.api_key = 'sua_chave_api_chatgpt'

def ask_chatgpt(question):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()
''',

    'app/services/db_service.py': '''from flask_mysqldb import MySQL
from . import mysql

def fetch_insemination_data():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM inseminacao")
    records = cursor.fetchall()
    db_info = "\\n".join([f"ID: {row[0]}, Data: {row[1]}, Valor: {row[2]}" for row in records])
    return db_info
''',

    'app/templates/home.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT - Inseminação</title>
</head>
<body>
    <h1>ChatGPT - Inseminação</h1>
    <form id="chatForm">
        <input type="text" id="question" placeholder="Faça sua pergunta...">
        <button type="submit">Enviar</button>
    </form>
    <div id="response"></div>

    <script>
        document.getElementById('chatForm').onsubmit = async function(event) {
            event.preventDefault();
            const question = document.getElementById('question').value;

            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question })
            });

            const data = await response.json();
            document.getElementById('response').innerText = data.response;
        }
    </script>
</body>
</html>
''',

    'config.py': '''import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'seu_usuario_mysql'
    MYSQL_PASSWORD = 'sua_senha_mysql'
    MYSQL_DB = 'inseminacao'
''',

    'run.py': '''from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
''',

    'requirements.txt': '''Flask
Flask-MySQLdb
openai
'''
}

# Criar pastas
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Criar arquivos com conteúdo
for file, content in files.items():
    with open(file, 'w') as f:
        f.write(content)

print("Estrutura do projeto Flask criada com sucesso!")
