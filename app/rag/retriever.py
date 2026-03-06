# app/rag/retriever.py

from app.database.connection import get_connection
from app.config import TOP_K


def retrieve_similar(query_embedding, k=TOP_K):
    """
    Retrieve top-k similar documents from knowledge_chunks
    using cosine distance.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT content,
               embedding <=> %s::vector AS distance
        FROM knowledge_chunks
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
    """, (query_embedding, query_embedding, k))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results