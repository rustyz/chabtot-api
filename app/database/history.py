from app.database.connection import get_connection

def save_chat(session_id, user_message, bot_response):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (session_id, user_message, bot_response)
        VALUES (%s, %s, %s)
    """, (session_id, user_message, bot_response))

    conn.commit()
    cursor.close()
    conn.close()


def save_review_question(question, reason="low_confidence"):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO review_questions (question, reason)
        VALUES (%s, %s)
    """, (question, reason))

    conn.commit()
    cursor.close()
    conn.close()