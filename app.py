import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_history = [
    {"role": "system", "content": "You are a helpful, intelligent AI assistant."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
        
    chat_history.append({"role": "user", "content": user_input})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="openai/gpt-oss-20b", 
        )
        
        assistant_response = chat_completion.choices[0].message.content
        
        chat_history.append({"role": "assistant", "content": assistant_response})
        
        return jsonify({"response": assistant_response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)