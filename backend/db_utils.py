import psycopg2
import os
import logging
import uuid

logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        database_url = os.getenv('DATABASE_URL', 'postgresql://chatbot:chatbot123@localhost:5432/chatbot_db')
        return psycopg2.connect(database_url)
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        return None

def save_chat(session_id, user_message, bot_response, document_context=None):
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chats (session_id, user_message, bot_response, document_context) VALUES (%s, %s, %s, %s) RETURNING id",
            (session_id, user_message, bot_response, document_context)
        )
        chat_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return chat_id
    except Exception as e:
        logger.warning(f"Failed to save chat: {e}")
        conn.rollback()
        conn.close()
        return None

def get_chat_history(session_id):
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, user_message, bot_response, timestamp, document_context FROM chats WHERE session_id = %s ORDER BY timestamp",
            (session_id,)
        )
        chats = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [{
            'id': chat[0],
            'user_message': chat[1],
            'bot_response': chat[2],
            'timestamp': chat[3].isoformat(),
            'document_context': chat[4]
        } for chat in chats]
    except Exception as e:
        logger.warning(f"Failed to get chat history: {e}")
        conn.close()
        return []

def get_session_document_context(session_id):
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT document_context FROM chats WHERE session_id = %s AND document_context IS NOT NULL ORDER BY timestamp DESC LIMIT 1",
            (session_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        logger.warning(f"Failed to get document context: {e}")
        conn.close()
        return None

def get_sessions():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT session_id FROM chats ORDER BY session_id")
        sessions = cursor.fetchall()
        cursor.close()
        conn.close()
        return [session[0] for session in sessions]
    except Exception as e:
        logger.warning(f"Failed to get sessions: {e}")
        conn.close()
        return []