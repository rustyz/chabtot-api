from app.database.connection import get_connection
from app.embeddings.embedder import get_embedding

def save_manual_knowledge(question, answer):
    conn = get_connection()
    cursor = conn.cursor()

    embedding = get_embedding(answer)

    cursor.execute("""
        INSERT INTO manual_knowledge (question, answer, embedding)
        VALUES (%s, %s, %s::vector)
    """, (question, answer, embedding))

    conn.commit()
    cursor.close()
    conn.close()