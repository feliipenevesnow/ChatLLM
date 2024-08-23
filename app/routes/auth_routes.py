from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.user_service import authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        session.clear()

        user = authenticate_user(email, password)
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            return redirect(url_for('main.index'))
        else:
            flash('Credenciais inválidas. Por favor, tente novamente.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def logout_user():
    session.clear()
