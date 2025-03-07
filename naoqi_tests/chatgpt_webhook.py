from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenAI API Key
OPENAI_API_KEY = os.getenv("AI_STORYTELLER_TEST_KEY_CV")  # Uses environment variable for security

# Function to generate a story using OpenAI API
def generate_story(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    
    headers = {
        "Authorization": "Bearer " + OPENAI_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system", "content": "Tell a short children's story about " + prompt}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Error: Unable to generate story."

# Webhook Endpoint
@app.route("/generate_story", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data.get("word", "an adventure")

    story = generate_story(user_input)

    return jsonify({"story": story})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
