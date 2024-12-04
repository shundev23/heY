from flask import Flask, render_template, request, jsonify

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template("index.html", title="heY Chatbot")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please Enter a valid message."}), 400
     
    bot_reply = "You said: " + user_input
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)