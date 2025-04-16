from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os  # Make sure to import os module

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure random string

# Initialize conversation if not present
def init_conversation():
    session["conversation"] = [
        {
            "role": "system",
            "content": (
                "You are MHC, a caring, empathetic, supportive chatbot who "
                "remembers the conversation during the session. You are friendly and "
                "always try to help the user feel better by referring back to previous topics. "
                "Never mention that you don't remember past conversation."
            )
        }
    ]

@app.route("/")
def home():
    init_conversation()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    # Ensure conversation exists
    if "conversation" not in session:
        init_conversation()
    
    # Append the user's new message to the conversation history
    conversation = session["conversation"]
    conversation.append({"role": "user", "content": user_message})
    
    payload = {
        "model": "llama3",  # change this if you're using a different model in Ollama
        "messages": conversation,
        "stream": False  # Using non-streaming to get a complete single response
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        data = response.json()
        reply = data.get("message", {}).get("content", "I'm sorry, I didn't understand that.")
    except Exception as e:
        print("Error:", e)
        reply = "Sorry, something went wrong. Please try again."

    # Append the bot's reply to the conversation history
    conversation.append({"role": "assistant", "content": reply})
    session["conversation"] = conversation  # update session

    return jsonify({"reply": reply})

# Run app on Render with dynamic port
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
