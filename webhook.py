from flask import Flask, request, jsonify
import openai 
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req_data = request.get_json()

        # Extract parameters from Dialogflow CX
        session_params = req_data.get("sessionInfo", {}).get("parameters", {})
        username = session_params.get("username", "Adventurer")
        theme = session_params.get("theme", "fantasy")
        moral = session_params.get("moral", "courage")

        # Construct a storytelling prompt
        prompt = (f"Create a short interactive story for {username} in a {theme} setting, "
                  f"where the story teaches a lesson about {moral}. Make it engaging and immersive.")

        # Call OpenAI's ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract AI response
        ai_response = response["choices"][0]["message"]["content"]

        # Send response back to Dialogflow CX
        return jsonify({
            "fulfillment_response": {
                "messages": [{"text": {"text": [ai_response]}}]
            }
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "fulfillment_response": {
                "messages": [{"text": {"text": ["Error processing request."]}}]
            }
        })

if __name__ == '__main__':
    app.run(port=3000)