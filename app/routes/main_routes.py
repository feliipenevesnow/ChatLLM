from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/chat')
def index():
    if 'loggedin' in session:
        return render_template('chat.html')
    else:
        return redirect(url_for('auth.login'))
