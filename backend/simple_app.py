from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re

app = Flask(__name__)
CORS(app)

# Simple emotion detection without ML model
def simple_emotion_detection(text):
    text = text.lower()
    
    # Emotion keywords
    emotions = {
        'joy': ['happy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'good', 'excellent'],
        'sadness': ['sad', 'depressed', 'unhappy', 'down', 'upset', 'not good', 'bad', 'terrible'],
        'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'hate'],
        'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'frightened'],
        'love': ['love', 'adore', 'cherish', 'affection', 'romantic'],
        'surprise': ['surprised', 'shocked', 'amazed', 'unexpected', 'wow']
    }
    
    # Check for negative phrases
    if re.search(r'not.*good|not.*well|not.*happy|feeling.*bad|feel.*bad', text):
        return 'sadness', 0.8
    
    # Find matching emotions
    for emotion, keywords in emotions.items():
        for keyword in keywords:
            if keyword in text:
                return emotion, 0.75
    
    return 'neutral', 0.6

# Quranic verses
quranic_verses = {
    "joy": {
        "verse": "فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًۭا",
        "translation": "Indeed, with hardship [will be] ease. (Surah Ash-Sharh 94:6)"
    },
    "sadness": {
        "verse": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ ٱلْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ",
        "translation": "So do not weaken and do not grieve, and you will be superior if you are [true] believers. (Surah Al-Imran 3:139)"
    },
    "anger": {
        "verse": "وَٱلْكَـٰظِمِينَ ٱلْغَيْظَ وَٱلْعَافِينَ عَنِ ٱلنَّاسِ",
        "translation": "Those who restrain anger and who pardon the people – and Allah loves the doers of good. (Surah Al-Imran 3:134)"
    },
    "fear": {
        "verse": "إِنَّ ٱللَّهَ مَعَ ٱلصَّـٰبِرِينَ",
        "translation": "Indeed, Allah is with the patient. (Surah Al-Baqarah 2:153)"
    },
    "love": {
        "verse": "إِنَّ ٱلَّذِينَ آمَنُوا۟ وَعَمِلُوا۟ ٱلصَّـٰلِحَـٰتِ سَيَجْعَلُ لَهُمُ ٱلرَّحْمَـٰنُ وُدًّۭا",
        "translation": "Indeed, those who have believed and done righteous deeds – the Most Merciful will appoint for them affection. (Surah Maryam 19:96)"
    },
    "surprise": {
        "verse": "وَمَا تَدْرِى نَفْسٌۭ مَّاذَا تَكْسِبُ غَدًۭا",
        "translation": "And no soul knows what it will earn tomorrow. (Surah Luqman 31:34)"
    },
    "neutral": {
        "verse": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ ۚ لَهُ ٱلْأَسْمَآءُ ٱلْحُسْنَىٰ",
        "translation": "Allah – there is no deity except Him. To Him belong the best names. (Surah Ta-Ha 20:8)"
    }
}

emotion_trend = {}

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "EmotionEye API is running",
        "version": "2.0.0-simple",
        "status": "active"
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({"error": "No message provided."}), 400
        
        emotion, confidence = simple_emotion_detection(message)
        
        # Update trend
        emotion_trend[emotion] = emotion_trend.get(emotion, 0) + 1
        
        verse_data = quranic_verses.get(emotion, quranic_verses['neutral'])
        
        replies = {
            "joy": "I sense happiness in your words! May your joy continue to flourish. 😊",
            "sadness": "I'm sorry you're feeling this way. Remember that difficult times pass. 💙",
            "anger": "I understand your frustration. Taking a moment to breathe can help. 😤",
            "fear": "It's okay to feel afraid sometimes. Courage means moving forward despite fear. 🤝",
            "love": "That's so heartwarming to hear! Love is one of life's greatest blessings. ❤️",
            "surprise": "Wow, that sounds unexpected! Life's surprises often bring growth. 😲",
            "neutral": "Thanks for sharing. I'm here to listen whenever you're ready to explore further. 🙂"
        }
        
        return jsonify({
            "emotion": emotion,
            "confidence": confidence,
            "reply": replies.get(emotion, replies["neutral"]),
            "quranic_aayat": verse_data["verse"],
            "translation": verse_data["translation"]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sentiment-trend', methods=['GET'])
def get_sentiment_trend():
    all_emotions = ['joy', 'sadness', 'anger', 'fear', 'love', 'surprise', 'neutral']
    trend_data = {emotion: emotion_trend.get(emotion, 0) for emotion in all_emotions}
    return jsonify(trend_data)

if __name__ == '__main__':
    print("Starting EmotionEye Simple API on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)