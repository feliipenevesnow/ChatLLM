from flask import g
import MySQLdb.cursors
from app.models.chat import Chat

class ChatRepository:
    @staticmethod
    def create_chat(user_id, title):
        if len(title) > 100:
            title = title[:100] + '...'

        cursor = g.mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO chats (user_id, title) VALUES (%s, %s)', (user_id, title)
        )
        g.mysql.connection.commit()
        chat_id = cursor.lastrowid
        cursor.close()
        return Chat(chat_id, user_id, title)

    @staticmethod
    def update_chat_title(chat_id, new_title):
        if len(new_title) > 100:
            new_title = new_title[:100] + '...'

        cursor = g.mysql.connection.cursor()
        cursor.execute(
            'UPDATE chats SET title = %s WHERE id = %s',
            (new_title, chat_id)
        )
        g.mysql.connection.commit()
        cursor.close()

    @staticmethod
    def get_chat_by_id(chat_id):
        cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM chats WHERE id = %s', (chat_id,))
        chat_data = cursor.fetchone()
        cursor.close()
        if chat_data:
            return Chat(**chat_data)
        return None

    @staticmethod
    def get_chats_by_user(user_id):
        cursor = g.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM chats WHERE user_id = %s', (user_id,))
        chats_data = cursor.fetchall()
        cursor.close()
        return [Chat(**chat) for chat in chats_data]

    @staticmethod
    def delete_chat(chat_id):
        cursor = g.mysql.connection.cursor()
        cursor.execute('DELETE FROM chats WHERE id = %s', (chat_id,))
        g.mysql.connection.commit()
        cursor.close()
