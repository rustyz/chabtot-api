# app/embeddings/embedder.py

from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL_NAME


# Load model once globally
model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text: str):
    return model.encode(text).tolist()