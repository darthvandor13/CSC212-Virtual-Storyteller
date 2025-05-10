##! @file webhook.py
##! @brief  Dialogflow CX webhook that returns a short, themed children’s story.
##! @author Calvin Vandor

from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Extract parameters from Dialogflow CX
        params   = request.get_json().get("sessionInfo", {}).get("parameters", {})
        username = params.get("username", "Adventurer")
        theme    = params.get("theme",    "fantasy")
        moral    = params.get("moral",    "courage")

        # Build a prompt and call OpenAI
        prompt = (f"Create a short interactive story for {username} in a {theme} setting, "
                  f"where the story teaches a lesson about {moral}. Make it engaging and immersive.")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_text = response["choices"][0]["message"]["content"]

        # Send result back to Dialogflow CX
        return jsonify({
            "fulfillment_response": {
                "messages": [{"text": {"text": [ai_text]}}]
            }
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "fulfillment_response": {
                "messages": [{"text": {"text": ["Error processing request."]}}]
            }
        })

if __name__ == "__main__":
    app.run(port=3000)

