# -*- coding: utf-8 -*-

import markdown2
from flask import Blueprint, request, jsonify, session
from app.services.message_service import MessageService
from app.services.gemini_service import GeminiService
from app.services.chat_service import ChatService
from app.models.message_history import MessageHistory
import re

message_bp = Blueprint('message', __name__)
gemini_service = GeminiService()

@message_bp.route('/<int:chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    messages = MessageService.get_messages_by_chat(chat_id)
    return jsonify([message.__dict__ for message in messages])

@message_bp.route('/<int:chat_id>/messages', methods=['POST'])
def create_message(chat_id):
    try:
        data = request.get_json()

        message_history = MessageHistory()
        message_history.history = session.get('message_history', [])

        ChatService.update_chat_title_if_default(chat_id, data['message_text'])

        history_formatted = "\n".join(
            [f"{sender_type}: {re.sub('<[^>]*>', '', message)}" for sender_type, message in
             message_history.format_history_for_prompt()]
        )

        ai_response = gemini_service.process_message(data['message_text'], history_formatted)

        message_history.update_history('user', data['message_text'])

        message_history.update_history('ai', ai_response)

        user_message = MessageService.create_message(chat_id, 'user', data['message_text'])
        if not user_message:
            return jsonify({"error": "Falha ao salvar a mensagem"}), 500

        ai_message = MessageService.create_message(chat_id, 'ai', markdown2.markdown(ai_response))
        if not ai_message:
            return jsonify({"error": "Falha ao salvar a resposta da IA"}), 500

        session['message_history'] = message_history.history

        return jsonify({
            "user_message": user_message.__dict__,
            "ai_message": ai_message.__dict__
        })
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return jsonify({"error": str(e)}), 500
