from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.user_service import add_user, authenticate_user, get_user_by_email

register_bp = Blueprint('register', __name__)


@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash('As senhas não conferem!', 'danger')
        elif get_user_by_email(email):
            flash('Usuário já existe!', 'danger')
        else:

            session.clear()


            add_user(first_name, last_name, email, password)
            user = authenticate_user(email, password)

            if user:
                session['loggedin'] = True
                session['id'] = user['id']
                session['email'] = user['email']
                session['first_name'] = user['first_name']
                session['last_name'] = user['last_name']
                return redirect(url_for('main.index'))

            flash('Cadastro realizado com sucesso!', 'success')
    return render_template('register.html')
