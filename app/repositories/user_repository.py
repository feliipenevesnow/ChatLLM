import MySQLdb.cursors
from flask import g
from werkzeug.security import generate_password_hash
from app.models.user import User

class UserRepository:
    @staticmethod
    def authenticate(email, password):
        cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            user_data.pop('created_at', None)
            user = User(**user_data)
            if user.check_password(password):
                return user
        return None

    @staticmethod
    def add(first_name, last_name, email, password):
        hashed_password = generate_password_hash(password)
        cursor = g.mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
            (first_name, last_name, email, hashed_password)
        )
        g.mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_by_email(email):
        cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            return User(**user_data)
        return None

    @staticmethod
    def update_theme(user_id, theme):
        cursor = g.mysql.connection.cursor()
        cursor.execute(
            'UPDATE users SET theme = %s WHERE id = %s',
            (theme, user_id)
        )
        g.mysql.connection.commit()
        cursor.close()
