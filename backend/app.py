from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# Load emotion detection model
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

@app.route('/', methods=['GET'])
def home():
    return "🎯 EmotionEye API is running."

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        result = classifier(user_message)[0]
        emotion = result["label"]  # e.g., joy, anger, sadness
        score = round(result["score"], 2)
        reply = generate_bot_reply(emotion)

        return jsonify({
            "emotion": emotion,
            "confidence": score,
            "reply": reply
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_bot_reply(emotion):
    if emotion == "joy":
        return "You sound so happy! What's got you in such a great mood? 😊"
    elif emotion == "anger":
        return "I can sense you're upset. Let's figure out what's wrong. 😔"
    elif emotion == "sadness":
        return "I'm sorry you're feeling down. I'm here to listen. 💙"
    else:
        return "Let's talk more about how you're feeling!"

if __name__ == '__main__':
    app.run(debug=True)