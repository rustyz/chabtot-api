from flask import Flask, request, jsonify
from flask_cors import CORS

from app.chat.chat_service import process_query
from app.config import ENV

app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json

    question = data.get("question")
    session_id = data.get("session_id")

    if not question:
        return jsonify({"error": "Question required"}), 400

    result = process_query(
        question,
        debug=(ENV == "TEST"),
        session_id=session_id
    )

    # TEST environment returns debugging info
    if ENV == "TEST":
        return jsonify(result)

    # PROD environment returns only answer
    return jsonify({
        "answer": result["answer"]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "environment": ENV
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)