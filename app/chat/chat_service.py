import uuid

from app.embeddings.embedder import get_embedding
from app.rag.retriever import retrieve_similar
from app.rag.manual_retriever import retrieve_manual
from app.llm.qa_model import generate_answer
from app.database.history import save_chat, save_review_question


def process_query(question, debug=False, session_id=None):

    if session_id is None:
        session_id = str(uuid.uuid4())

    # Generate embedding
    query_embedding = get_embedding(question)

    # ==========================================
    # STEP 1: CHECK MANUAL KNOWLEDGE
    # ==========================================
    manual_answer, manual_type = retrieve_manual(question, query_embedding)

    if manual_answer:
        save_chat(session_id, question, manual_answer)

        return {
            "answer": manual_answer,
            "retrieved_docs": [],
            "source": f"manual_{manual_type}"
        }

    # ==========================================
    # STEP 2: RETRIEVE FROM KNOWLEDGE CHUNKS
    # ==========================================
    retrieved_docs = retrieve_similar(query_embedding)

    if not retrieved_docs:
        save_review_question(question, "no_docs")
        return {
            "answer": "No relevant information found.",
            "retrieved_docs": [],
            "source": "none"
        }

    # Build context
    context = "\n\n".join([doc[0] for doc in retrieved_docs])

    prompt = f"""
You are an assistant for IDEAM.

Using ONLY the context below,
answer the question in one clear, professional sentence.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate_answer(prompt).strip()

    # Ensure proper sentence ending
    if not answer.endswith("."):
        answer += "."

    # If weak answer → log for review
    if len(answer.split()) < 5:
        save_review_question(question, "weak_answer")

    # Save chat history
    save_chat(session_id, question, answer)

    return {
        "answer": answer,
        "retrieved_docs": retrieved_docs,
        "source": "knowledge_chunks"
    }