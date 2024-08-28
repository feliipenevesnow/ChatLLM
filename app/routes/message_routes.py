import markdown2
from flask import Blueprint, request, jsonify, session
from app.services.message_service import MessageService
from app.services.gemini_service import GeminiService
from app.services.chat_service import ChatService
from app.models.message_history import MessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


message_bp = Blueprint('message', __name__)
gemini_service = GeminiService()  # Inicializando o serviço Gemini

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

        print(f"Recebendo mensagem: {data['message_text']} para o chat {chat_id}")

        user_message = MessageService.create_message(chat_id, data['sender_type'], data['message_text'])
        if not user_message:
            return jsonify({"error": "Falha ao salvar a mensagem"}), 500

        message_history.update_history(data['message_text'], "")  # Somente atualiza com a mensagem do usuário

        print(message_history.format_history_for_prompt())

        # Preparar o prompt no novo formato
        prompt = ChatPromptTemplate.from_messages(
            message_history.format_history_for_prompt() +
            [("user", data['message_text'])]
        )

        ai_response_markdown = gemini_service.generate_response_with_retry(prompt)
        ai_response_html = markdown2.markdown(ai_response_markdown)

        ai_message = MessageService.create_message(chat_id, 'ai', ai_response_html)
        if not ai_message:
            return jsonify({"error": "Falha ao salvar a resposta da IA"}), 500

        session['message_history'] = message_history.history  # Atualiza o histórico na sessão

        return jsonify({
            "user_message": user_message.__dict__,
            "ai_message": ai_message.__dict__
        })
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return jsonify({"error": str(e)}), 500
