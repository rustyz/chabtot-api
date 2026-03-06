# app/chat/review_detector.py

from app.config import REVIEW_DISTANCE_THRESHOLD
from app.database.connection import get_connection


def should_flag_for_review(results):
    """
    Flag question if similarity distance is too high
    (meaning weak match in knowledge base).
    """
    if not results:
        return True

    # results = [(content, distance), ...]
    best_distance = results[0][1]

    return best_distance > REVIEW_DISTANCE_THRESHOLD


def save_review_question(question_text: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO review_questions (question_text)
        VALUES (%s);
    """, (question_text,))

    conn.commit()
    cursor.close()
    conn.close()