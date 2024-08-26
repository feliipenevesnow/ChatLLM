import random
from flask import Blueprint, request, jsonify
from app.services.message_service import MessageService

message_bp = Blueprint('message', __name__)

AI_MESSAGES = [
    "Bom dia, estou bem!",
    "Sim, eu gostaria de te ajudar.",
    "Como posso te auxiliar hoje?",
    "Estou aqui para ajudar com qualquer coisa que voce precisar.",
    "Que bom que voce esta aqui!",
    "Vamos resolver isso juntos!",
    "Estou pensando em uma solucao para isso.",
    "Essa e uma otima pergunta!",
    "Estou aqui para qualquer duvida que voce tiver.",
    "Vamos em frente, estou aqui para ajudar."
]


@message_bp.route('/<int:chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    messages = MessageService.get_messages_by_chat(chat_id)
    return jsonify([message.__dict__ for message in messages])

@message_bp.route('/<int:chat_id>/messages', methods=['POST'])
def create_message(chat_id):
    try:
        data = request.get_json()
        print(f"Recebendo mensagem: {data['message_text']} para o chat {chat_id}")

        user_message = MessageService.create_message(chat_id, data['sender_type'], data['message_text'])
        if not user_message:
            print("Erro ao salvar a mensagem do usuario")
            return jsonify({"error": "Falha ao salvar a mensagem"}), 500

        ai_response_text = random.choice(AI_MESSAGES)
        ai_message = MessageService.create_message(chat_id, 'api', ai_response_text)
        if not ai_message:
            print("Erro ao salvar a resposta da IA")
            return jsonify({"error": "Falha ao salvar a resposta da IA"}), 500

        print("Mensagens salvas com sucesso")
        return jsonify({
            "user_message": user_message.__dict__,
            "ai_message": ai_message.__dict__
        })
    except Exception as e:
        print(f"Erro durante o processamento: {e}")
        return jsonify({"error": str(e)}), 500


