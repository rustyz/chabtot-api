from flask import Flask, request, jsonify
from flask_cors import CORS

from app.chat.chat_service import process_query
from app.config import ENV

app = Flask(__name__)
CORS(app)


@app.route("/chat", methods=["POST"])
def chat():

    try:
        # Safely parse JSON body
        data = request.get_json(force=True)

        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Extract fields safely
        question = data.get("question", "").strip()
        session_id = data.get("session_id", "web_user")

        if not question:
            return jsonify({"error": "Question required"}), 400

        # Process query through RAG pipeline
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

    except Exception as e:

        print("CHAT ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "environment": ENV
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)