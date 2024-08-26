from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from app.services.chat_service import ChatService
from app.services.message_service import MessageService

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/')
def index():
    user_id = session.get('id')
    if not user_id:
        return redirect(url_for('user.login'))

    chats = ChatService.get_chats_by_user(user_id)
    return render_template('chat.html', chats=chats)

@chat_bp.route('/create', methods=['POST'])
def create_chat():
    user_id = session.get('id')
    title = "Novo Chat"
    chat = ChatService.create_chat(user_id, title)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes.best == 'application/json':
        return jsonify({'chat_id': chat.id})
    else:
        return redirect(url_for('chat.view_chat', chat_id=chat.id))

@chat_bp.route('/<int:chat_id>')
def view_chat(chat_id):
    chat = ChatService.get_chat_by_id(chat_id)
    messages = MessageService.get_messages_by_chat(chat_id)
    chats = ChatService.get_chats_by_user(session.get('id'))
    return render_template('chat.html', chats=chats, messages=messages)

@chat_bp.route('/<int:chat_id>/update', methods=['POST'])
def update_chat(chat_id):
    data = request.get_json()
    new_title = data.get('title')
    if new_title:
        ChatService.update_chat_title(chat_id, new_title)
    return '', 204

@chat_bp.route('/<int:chat_id>/delete', methods=['POST'])
def delete_chat(chat_id):
    try:
        MessageService.delete_messages_by_chat(chat_id)
        ChatService.delete_chat(chat_id)
        return redirect(url_for('chat.index'))
    except Exception as e:
        print(f"Erro ao deletar o chat: {e}")
        return redirect(url_for('chat.index'))
