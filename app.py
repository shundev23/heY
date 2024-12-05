from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import random

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

# 感情に基づく応答テンプレート
RESPONSES = {
    'very_positive': [
        "That's wonderful to hear! Your positivity is contagious! 🌟",
        "I'm absolutely thrilled for you! Keep that amazing spirit! ✨",
        "Fantastic! Your enthusiasm really brightens up our conversation! 🎉",
        "That's such great news! I'm genuinely happy for you! 💫"
    ],
    'positive': [
        "That's good to hear! Thanks for sharing that with me. 😊",
        "I'm glad things are going well! Keep it up! 👍",
        "That's nice! Your positive attitude is appreciated. 🌱",
        "Sounds promising! I'm here to support your journey. ⭐"
    ],
    'neutral': [
        "I understand. Would you like to tell me more about that?",
        "Interesting perspective. How does that make you feel?",
        "I see. What are your thoughts on this?",
        "Thank you for sharing. Is there anything specific you'd like to discuss?"
    ],
    'negative': [
        "I hear you. It's okay to feel this way. Would you like to talk about it? 🌧",
        "That sounds challenging. I'm here to listen if you need support. 🍃",
        "I'm sorry you're going through this. How can I help? 💭",
        "Things can be tough sometimes. Let's work through this together. 🤝"
    ],
    'very_negative': [
        "I'm really sorry you're feeling this way. Remember, you're not alone. 💗",
        "That must be really difficult. Please know that I'm here to support you. 🫂",
        "It's completely valid to feel this way. Would you like to talk more about it? 🌈",
        "I'm here for you during this tough time. What would help you feel better? 💝"
    ]
}

def get_response_category(sentiment_score):
    if sentiment_score >= 0.5:
        return 'very_positive'
    elif 0.1 <= sentiment_score < 0.5:
        return 'positive'
    elif -0.1 < sentiment_score < 0.1:
        return 'neutral'
    elif -0.5 <= sentiment_score <= -0.1:
        return 'negative'
    else:
        return 'very_negative'

def analyze_context(text):
    keywords = {
        'question': ['?', 'what', 'how', 'why', 'when', 'where', 'who'],
        'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
        'gratitude': ['thank', 'thanks', 'appreciate'],
        'farewell': ['bye', 'goodbye', 'see you', 'later']
    }
    
    text = text.lower()
    for context, words in keywords.items():
        if any(word in text for word in words):
            return context
    return 'general'

@app.route('/')
def index():
    return render_template("index.html", title="heY Chatbot")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please Enter a valid message."}), 400

    # 感情分析
    analysis = TextBlob(user_input)
    sentiment_score = analysis.sentiment.polarity
    
    # 文脈分析
    context = analyze_context(user_input)
    
    # 応答カテゴリの決定
    category = get_response_category(sentiment_score)
    
    # 応答の選択
    bot_reply = random.choice(RESPONSES[category])
    
    # 文脈に応じた追加応答
    if context == 'question':
        bot_reply += "\nLet me help you find an answer."
    elif context == 'greeting':
        bot_reply = "Hello! 👋 " + bot_reply
    elif context == 'gratitude':
        bot_reply += "\nYou're welcome! 😊"
    elif context == 'farewell':
        bot_reply += "\nTake care! Hope to chat again soon! 👋"

    return jsonify({
        "response": bot_reply,
        "sentiment": sentiment_score,
        "context": context
    })

if __name__ == "__main__":
    app.run(debug=True)