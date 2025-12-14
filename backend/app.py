from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from collections import defaultdict
import re
import random
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, origins=["*"])  # Configure CORS for production

# Load emotion classification model with caching
model_name = os.getenv('MODEL_NAME', 'bhadresh-savani/distilbert-base-uncased-emotion')
cache_dir = os.getenv('MODEL_CACHE_DIR', './model_cache')

try:
    classifier = pipeline(
        "text-classification",
        model=model_name,
        cache_dir=cache_dir
    )
    print(f"✅ Model loaded successfully: {model_name}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise e

# Emotion trend tracking
emotion_trend = defaultdict(int)

# Sample Quranic verses and meanings mapped to emotions
quranic_verses = {
    "joy": {
        "verse": "فَإِنَّ مَعَ ٱلْعُسْرِ يُسْرًۭا",
        "translation": "Indeed, with hardship [will be] ease. (Surah Ash-Sharh 94:6)",
        "bangla": "নিশ্চয়ই কষ্টের সাথে রয়েছে স্বস্তি। (সূরা আশ-শারহ ৯৪:৬)"
    },
    "sadness": {
        "verse": "وَلَا تَهِنُوا وَلَا تَحْزَنُوا وَأَنتُمُ ٱلْأَعْلَوْنَ إِن كُنتُم مُّؤْمِنِينَ",
        "translation": "So do not weaken and do not grieve, and you will be superior if you are [true] believers. (Surah Al-Imran 3:139)",
        "bangla": "তোমরা দুর্বল হয়ো না এবং দুঃখ করো না; যদি তোমরা মুমিন হও, তবে তোমরাই শ্রেষ্ঠ। (سورة آل عمران ٣:١٣٩)"
    },
    "anger": {
        "verse": "وَٱلْكَـٰظِمِينَ ٱلْغَيْظَ وَٱلْعَافِينَ عَنِ ٱلنَّاسِ",
        "translation": "Those who restrain anger and who pardon the people – and Allah loves the doers of good. (Surah Al-Imran 3:134)",
        "bangla": "যারা রাগ সংবরণ করে এবং মানুষকে ক্ষমা করে – আল্লাহ সৎকর্মশীলদের ভালবাসেন। (سورة آل عمران ٣:١٣٤)"
    },
    "fear": {
        "verse": "إِنَّ ٱللَّهَ مَعَ ٱلصَّـٰبِرِينَ",
        "translation": "Indeed, Allah is with the patient. (Surah Al-Baqarah 2:153)",
        "bangla": "নিশ্চয়ই আল্লাহ ধৈর্যশীলদের সাথে আছেন। (سورة البقرة ٢:١٥٣)"
    },
    "love": {
        "verse": "إِنَّ ٱلَّذِينَ آمَنُوا۟ وَعَمِلُوا۟ ٱلصَّـٰلِحَـٰتِ سَيَجْعَلُ لَهُمُ ٱلرَّحْمَـٰنُ وُدًّۭا",
        "translation": "Indeed, those who have believed and done righteous deeds – the Most Merciful will appoint for them affection. (Surah Maryam 19:96)",
        "bangla": "নিশ্চয়ই যারা ঈমান এনেছে এবং সৎকর্ম করেছে, দয়াময় তাদের জন্য ভালোবাসা সৃষ্টি করবেন। (سورة مريم ١٩:٩٦)"
    },
    "surprise": {
        "verse": "وَمَا تَدْرِى نَفْسٌۭ مَّاذَا تَكْسِبُ غَدًۭا",
        "translation": "And no soul knows what it will earn tomorrow. (Surah Luqman 31:34)",
        "bangla": "কোন প্রাণ জানে না আগামীকাল সে কী অর্জন করবে। (سورة لقمان ٣١:٣٤)"
    },
    "neutral": {
        "verse": "ٱللَّهُ لَآ إِلَـٰهَ إِلَّا هُوَ ۚ لَهُ ٱلْأَسْمَآءُ ٱلْحُسْنَىٰ",
        "translation": "Allah – there is no deity except Him. To Him belong the best names. (Surah Ta-Ha 20:8)",
        "bangla": "আল্লাহ – তিনি ছাড়া কোনো উপাস্য নেই। সুন্দর নামসমূহ তাঁরই। (سورة طه ٢٠:٨)"
    }
}

# Negative phrase patterns to help correct misclassifications
NEGATIVE_PATTERNS = [
    r"not.*good", r"not.*well", r"not.*feel.*good", r"not.*ok", r"not.*okay",
    r"not.*happy", r"not.*great", r"not.*fine", r"feeling.*bad", r"feel.*bad",
    r"unhappy", r"upset", r"depressed", r"anxious", r"stressed", r"worried",
    r"sad", r"miserable", r"terrible", r"awful", r"horrible", r"hate"
]

def contains_negative_phrase(text):
    """Check if text contains negative emotion indicators"""
    text = text.lower()
    for pattern in NEGATIVE_PATTERNS:
        if re.search(pattern, text):
            return True
    return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "🎯 EmotionEye API is running",
        "version": "2.0.0",
        "status": "active",
        "environment": os.getenv('FLASK_ENV', 'development'),
        "features": [
            "Emotion analysis with DistilBERT",
            "Quranic guidance integration",
            "Negative phrase detection",
            "Sentiment trend tracking"
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Test model availability
        test_result = classifier("test")
        return jsonify({
            "status": "healthy",
            "model_loaded": True,
            "timestamp": str(datetime.now())
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e),
            "timestamp": str(datetime.now())
        }), 503

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided."}), 400

        result = classifier(user_message)[0]
        emotion = result['label'].lower()
        confidence = round(result['score'], 2)
        
        # Check for negative phrases that might be misclassified as positive
        if emotion == "joy" and contains_negative_phrase(user_message):
            # Get second most likely emotion if joy seems incorrect
            all_results = classifier(user_message)
            if len(all_results) > 1:
                # Find the next best emotion that's not joy
                for res in all_results[1:]:
                    if res['label'].lower() != 'joy':
                        emotion = res['label'].lower()
                        confidence = round(res['score'], 2)
                        break
            else:
                # Default to sadness if no other options
                emotion = "sadness"
                confidence = 0.7  # Moderate confidence
        
        # Update emotion trend
        emotion_trend[emotion] += 1

        # Generate dynamic responses
        bot_reply = generate_bot_reply(emotion, user_message)
        verse_data = quranic_verses.get(emotion, quranic_verses['neutral'])

        return jsonify({
            "emotion": emotion,
            "confidence": confidence,
            "reply": bot_reply,
            "quranic_aayat": verse_data["verse"],
            "translation": verse_data["translation"],
            "original_classification": result['label'].lower()  # For debugging
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/sentiment-trend', methods=['GET'])
def get_sentiment_trend():
    # Ensure all emotion categories are present (even with zero counts)
    all_emotions = ['joy', 'sadness', 'anger', 'fear', 'love', 'surprise', 'neutral']
    trend_data = {emotion: emotion_trend.get(emotion, 0) for emotion in all_emotions}
    return jsonify(trend_data)

def generate_bot_reply(emotion, user_message):
    responses = {
        "joy": [
            "I sense happiness in your words! May your joy continue to flourish. 😊",
            "Your positive energy is uplifting! Remember to share this joy with others. 🌟",
            "It's wonderful to hear you're feeling joyful! Cherish these moments. ✨"
        ],
        "sadness": [
            "I'm sorry you're feeling this way. Remember that difficult times pass. 💙",
            "Your feelings are valid. It's okay to not be okay sometimes. 🌧️",
            "I hear the sadness in your words. You're not alone in this. 🤗"
        ],
        "anger": [
            "I understand your frustration. Taking a moment to breathe can help. 😤",
            "Anger is a natural emotion. Channeling it constructively is powerful. ⚡",
            "I sense your irritation. Let's work through these feelings together. 🌋"
        ],
        "fear": [
            "It's okay to feel afraid sometimes. Courage means moving forward despite fear. 🤝",
            "Your concerns are valid. Remember that you've overcome challenges before. 🛡️",
            "I hear the worry in your words. Let's break this down together. 🧩"
        ],
        "love": [
            "That's so heartwarming to hear! Love is one of life's greatest blessings. ❤️",
            "The love you're expressing is beautiful. Nurture these special feelings. 🌹",
            "Your words radiate affection! Cherish these meaningful connections. 💞"
        ],
        "surprise": [
            "Wow, that sounds unexpected! Life's surprises often bring growth. 😲",
            "Unexpected events can be unsettling. Let's process this together. 🔄",
            "Your surprise is understandable! Sometimes life takes unexpected turns. 🌈"
        ],
        "neutral": [
            "Thanks for sharing. I'm here to listen whenever you're ready to explore further. 🙂",
            "I appreciate you opening up. Let me know if you'd like to discuss anything specific. 🤔",
            "Your thoughts are valued. Feel free to share more about what's on your mind. 💭"
        ]
    }
    
    # Special case for corrected emotions
    if contains_negative_phrase(user_message) and emotion == "sadness":
        return "I notice you mentioned not feeling good. I'm here to support you through this. 💙"
    
    return random.choice(responses.get(emotion, responses["neutral"]))

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting EmotionEye API on {host}:{port}")
    app.run(debug=debug, host=host, port=port)