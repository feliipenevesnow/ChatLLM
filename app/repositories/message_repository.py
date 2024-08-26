from flask import g
import MySQLdb.cursors
from app.models.message import Message

class MessageRepository:
    @staticmethod
    def create_message(chat_id, sender_type, message_text):
        cursor = g.mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO messages (chat_id, sender_type, message_text) VALUES (%s, %s, %s)',
            (chat_id, sender_type, message_text)
        )
        g.mysql.connection.commit()
        message_id = cursor.lastrowid
        cursor.close()
        return Message(message_id, chat_id, sender_type, message_text)

    @staticmethod
    def get_messages_by_chat(chat_id):
        cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM messages WHERE chat_id = %s ORDER BY created_at ASC', (chat_id,))
        messages_data = cursor.fetchall()
        cursor.close()
        return [Message(**message) for message in messages_data]

    @staticmethod
    def delete_messages_by_chat(chat_id):
        cursor = g.mysql.connection.cursor()
        cursor.execute('DELETE FROM messages WHERE chat_id = %s', (chat_id,))
        g.mysql.connection.commit()
        cursor.close()
