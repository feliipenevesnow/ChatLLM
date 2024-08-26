from app.repositories.message_repository import MessageRepository

class MessageService:
    @staticmethod
    def create_message(chat_id, sender_type, message_text):
        return MessageRepository.create_message(chat_id, sender_type, message_text)

    @staticmethod
    def get_messages_by_chat(chat_id):
        return MessageRepository.get_messages_by_chat(chat_id)

    @staticmethod
    def delete_messages_by_chat(chat_id):
        return MessageRepository.delete_messages_by_chat(chat_id)
