import MySQLdb.cursors
from flask import g
from werkzeug.security import check_password_hash, generate_password_hash

def authenticate_user(email, password):
    cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user['password'], password):
        return user
    return None

def add_user(first_name, last_name, email, password):
    hashed_password = generate_password_hash(password)

    cursor = g.mysql.connection.cursor()
    cursor.execute('INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)',
                   (first_name, last_name, email, hashed_password))
    g.mysql.connection.commit()
    cursor.close()

def get_user_by_email(email):
    cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()
    return user
