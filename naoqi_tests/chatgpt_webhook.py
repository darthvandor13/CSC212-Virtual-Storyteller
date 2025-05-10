##! @file chatgpt_webhook.py
##! @brief  Flask webhook that turns a keyword into a children’s story.
##! @author Calvin Vandor

from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# OpenAI API Key (set via env var for security)
OPENAI_API_KEY = os.getenv("AI_STORYTELLER_TEST_KEY_CV")

def generate_story(prompt):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + OPENAI_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "system",
                      "content": "Tell a short children's story about " + prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return "Error: unable to generate story."

@app.route("/generate_story", methods=["POST"])
def webhook():
    user_input = request.get_json().get("word", "an adventure")
    story = generate_story(user_input)
    return jsonify({"story": story})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

