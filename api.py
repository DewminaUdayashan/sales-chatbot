from flask import Flask, request, jsonify
from chatbot import get_response, model, preprocess

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    chat_history = data.get("history", [])

    # Preprocess + predict intent + confidence
    processed = preprocess(message)
    predicted_prob = model.predict_proba([processed])[0]
    intent = model.predict([processed])[0]
    confidence = round(max(predicted_prob), 4)

    # Get response from logic
    raw_reply = get_response(message, chat_history)

    # Extract suggestions (if any vehicle listings exist)
    lines = raw_reply.split("\n")
    suggestions = []
    for line in lines[1:]:
        parts = line.rsplit(" (ID: ", 1)
        if len(parts) == 2:
            title = parts[0].strip()
            ad_id = parts[1].replace(")", "").strip()
            suggestions.append({
                "ad_id": ad_id,
                "title": title
            })

    return jsonify({
        "response": lines[0],  # first line is the main response
        "intent": intent,
        "confidence": confidence,
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(debug=True)