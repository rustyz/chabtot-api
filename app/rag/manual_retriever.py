from app.database.connection import get_connection

def retrieve_manual(question, query_embedding):

    conn = get_connection()
    cursor = conn.cursor()

    # 🔹 Step 1: Exact match (case insensitive)
    cursor.execute("""
        SELECT answer
        FROM manual_knowledge
        WHERE LOWER(question) = LOWER(%s)
        LIMIT 1;
    """, (question,))

    exact_match = cursor.fetchone()

    if exact_match:
        cursor.close()
        conn.close()
        return exact_match[0], "exact"

    # 🔹 Step 2: High similarity match
    cursor.execute("""
        SELECT question, answer,
               embedding <=> %s::vector AS distance
        FROM manual_knowledge
        ORDER BY embedding <=> %s::vector
        LIMIT 1;
    """, (query_embedding, query_embedding))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        question_text, answer, distance = result

        if distance < 0.25:  # strict threshold
            return answer, "similarity"

    return None, None