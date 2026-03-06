# app/config.py

import os

# Environment (for future prod/test separation)
#ENV = os.getenv("ENV", "TEST")

ENV = os.getenv("ENV", "PROD")

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "chatbot_test" if ENV == "TEST" else "chatbot_prod",
    "user": "postgres",
    "password": "postgres"
}

# Embedding model name
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"

# Retrieval settings
TOP_K = 3

# Review detection threshold (cosine distance)
# Lower = more similar
REVIEW_DISTANCE_THRESHOLD = 0.35