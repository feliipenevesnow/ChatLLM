from flask import Flask, g, redirect, url_for
from flask_mysqldb import MySQL
from app.routes.auth_routes import auth_bp
from app.routes.main_routes import main_bp
from app.routes.register_routes import register_bp

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
        return redirect(url_for('auth.login'))

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(register_bp)
    app.register_blueprint(main_bp)

    return app
