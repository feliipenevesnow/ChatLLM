from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services.user_service import authenticate_user, add_user, get_user_by_email, update_user_theme

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        session.clear()

        user = authenticate_user(email, password)
        if user:
            session['loggedin'] = True
            session['id'] = user.id
            session['email'] = user.email
            session['first_name'] = user.first_name
            session['last_name'] = user.last_name
            session['theme'] = user.theme
            return redirect(url_for('chat.index'))
        else:
            flash("Email ou senha inválidos. Por favor, tente novamente.", "warning")
            return redirect(url_for('user.login'))

    return render_template('login.html')

@user_bp.route('/register', methods=['GET', 'POST'])
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
                session['id'] = user.id
                session['email'] = user.email
                session['first_name'] = user.first_name
                session['last_name'] = user.last_name
                session['theme'] = user.theme
                return redirect(url_for('chat.index'))

            flash('Cadastro realizado com sucesso!', 'success')
    return render_template('register.html')

@user_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))

@user_bp.route('/update_theme', methods=['POST'])
def update_theme():
    print("oidjnaowidjnoiwajdmoaiwndoaiwndoaiwndoi")

    if 'id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 403

    user_id = session['id']
    data = request.get_json()
    new_theme = data.get('theme')

    print(new_theme)

    if new_theme in ['light', 'dark']:
        update_user_theme(user_id, new_theme)
        session['theme'] = new_theme
        return jsonify({'message': 'Tema atualizado com sucesso'})
    else:
        return jsonify({'error': 'Tema inválido'}), 400
