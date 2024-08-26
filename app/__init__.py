from flask import Flask, g, redirect, url_for
from flask_mysqldb import MySQL
from app.routes.user_routes import user_bp
from app.routes.chat_routes import chat_bp
from app.routes.message_routes import message_bp

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mysql.init_app(app)

    @app.before_request
    def before_request():
        g.mysql = mysql

    @app.route('/')
    def index():
        return redirect(url_for('user.login'))

    app.register_blueprint(user_bp)
    app.register_blueprint(chat_bp, url_prefix='/chats')
    app.register_blueprint(message_bp, url_prefix='/mensagens')

    return app
