import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'seu_usuario_mysql'
    MYSQL_PASSWORD = 'sua_senha_mysql'
    MYSQL_DB = 'inseminacao'
