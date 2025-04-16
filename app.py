from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    payload = {
        "model": "llama3",  # Or whatever model name you're using
        "messages": [
            {"role": "system", "content": "You're a cheerful, friendly, and supportive mental health companion named MHC. Be kind, warm, and encouraging in every response."},
            {"role": "user", "content": user_message}
        ],
        "stream": True
    }

    response = requests.post(
        "http://localhost:11434/api/chat",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        stream=True
    )

    reply = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "message" in data and "content" in data["message"]:
                reply += data["message"]["content"]

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
