"""
Ingest CSV chunks into PostgreSQL with embeddings
"""

import os
import pandas as pd
from app.database.connection import get_connection
from app.embeddings.embedder import get_embedding

# ===== PATH CONFIG =====

CURRENT_FILE = os.path.abspath(__file__)
DATABASE_DIR = os.path.dirname(CURRENT_FILE)
APP_DIR = os.path.dirname(DATABASE_DIR)
PROJECT_ROOT = os.path.dirname(APP_DIR)

CSV_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "ideam_chunks.csv")


def ingest_chunks():

    df = pd.read_csv(CSV_FILE)

    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        embedding = get_embedding(row["content"])

        cursor.execute("""
            INSERT INTO knowledge_chunks (page_url, title, content, embedding)
            VALUES (%s, %s, %s, %s::vector)
        """, (
            row["page_url"],
            row["title"],
            row["content"],
            embedding
        ))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Ingested {len(df)} chunks successfully.")