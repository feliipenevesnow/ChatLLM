from app.repositories.chat_repository import ChatRepository

class ChatService:
    @staticmethod
    def create_chat(user_id, title):
        return ChatRepository.create_chat(user_id, title)

    @staticmethod
    def get_chat_by_id(chat_id):
        return ChatRepository.get_chat_by_id(chat_id)

    @staticmethod
    def get_chats_by_user(user_id):
        return ChatRepository.get_chats_by_user(user_id)

    @staticmethod
    def delete_chat(chat_id):
        ChatRepository.delete_chat(chat_id)

    @staticmethod
    def update_chat_title(chat_id, new_title):
        ChatRepository.update_chat_title(chat_id, new_title)

    @staticmethod
    def update_chat_title_if_default(chat_id, first_message):
        chat = ChatRepository.get_chat_by_id(chat_id)
        if chat and chat.title == "Novo Chat":
            ChatRepository.update_chat_title(chat_id, first_message)
