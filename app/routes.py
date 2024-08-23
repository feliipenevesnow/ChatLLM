from flask import Blueprint, render_template, request, jsonify
import openai
from .services.db_service import fetch_insemination_data
from .services.chat_service import ask_chatgpt

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('home.html')

@bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')

    db_info = fetch_insemination_data()

    full_question = f"Com base nos seguintes dados do banco de inseminação:\n{db_info}\n\n{question}"

    response = ask_chatgpt(full_question)

    return jsonify({'response': response})
