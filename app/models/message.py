class Message:
    def __init__(self, id, chat_id, sender_type, message_text, created_at=None):
        self.id = id
        self.chat_id = chat_id
        self.sender_type = sender_type
        self.message_text = message_text
        self.created_at = created_at
