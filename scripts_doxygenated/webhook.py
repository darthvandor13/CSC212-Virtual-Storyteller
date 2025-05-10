##! @file webhook.py
##! @brief  Dialogflow CX fulfilment webhook that generates an interactive
##!         short story with OpenAI ChatCompletion.
##!
##! This version is reorganised into small, reusable functions so that
##! Doxygen can render clear parameter / return tables and call graphs while
##! preserving the original runtime behaviour (with error HTTP status corrected to 200 OK).
##!
##! @author Calvin Vandor
##! @date   2025-05-08
##! @copyright MIT License
##!
##! ### Environment variables
##! * **OPENAI_API_KEY** — secret API key for the ChatCompletion endpoint.
##!
##! ### Flask routes
##! * **POST /webhook** — primary Dialogflow CX fulfilment entry-point.
##!
##! ---

from __future__ import annotations

import os
from typing import Dict, Any

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import openai

load_dotenv()

#: OpenAI API secret (read once at import time)
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    print("⚠️ WARNING: OPENAI_API_KEY environment variable not set. OpenAI calls will fail.")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_prompt(username: str, theme: str, moral: str) -> str:
    """Craft the instructional prompt sent to ChatGPT.

    @param username: Recipient of the story (default *Adventurer*).
    @param theme:    Story genre / setting (e.g., *fantasy*, *sci-fi*).
    @param moral:    Core lesson to convey (e.g., *courage*).
    @return Prompt string ready for ChatCompletion.
    """
    return (
        f"Create a short interactive story for {username} in a {theme} setting, "
        f"where the story teaches a lesson about {moral}. Make it engaging and immersive."
    )


def call_chatgpt(prompt: str) -> str:
    """Send the prompt to OpenAI and return the model's reply.

    @param prompt: Fully-formed prompt as returned by :pyfunc:`build_prompt`.
    @raises openai.APIError: If the HTTP request to OpenAI fails or returns an error.
    @return The assistant's textual response.
    """
    if not openai.api_key:
        raise ValueError("OpenAI API key is not configured. Cannot make API calls.")
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini", # User confirmed this model is fine for now
        messages=[{"role": "user", "content": prompt}],
    )
    # Type checker might complain about indexing if response structure isn't fully known/typed by stubs
    # Assuming standard response structure from OpenAI
    return response["choices"][0]["message"]["content"] # type: ignore[index]


# ---------------------------------------------------------------------------
# Flask setup
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    """Factory that builds and returns the Flask application object."""

    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook_endpoint() -> Any:  # noqa: ANN401 (Flask view functions can return various types)
        """Dialogflow CX fulfilment route (expects JSON body)."""
        try:
            # Using force=True to attempt JSON parsing even if an incorrect mimetype is sent.
            # For Dialogflow, the mimetype should usually be application/json.
            body: Dict[str, Any] = request.get_json(force=True) # Consider silent=True if you want to handle non-JSON body more gracefully
            
            params = body.get("sessionInfo", {}).get("parameters", {})
            username = params.get("username", "Adventurer")
            theme = params.get("theme", "fantasy")
            moral = params.get("moral", "courage")

            prompt = build_prompt(username, theme, moral)
            story_text = call_chatgpt(prompt)

            return jsonify(
                {
                    "fulfillment_response": {
                        "messages": [{"text": {"text": [story_text]}}]
                    }
                }
            )
        except Exception as exc:  # Broad catch to ensure some response is always sent
            print(f"❌ Webhook error: {exc}")
            import traceback
            traceback.print_exc() # Log full traceback for server-side debugging
            
            # Return HTTP 200 OK with the error message in the JSON payload
            # This is typically preferred by Dialogflow.
            return jsonify(
                {
                    "fulfillment_response": {
                        "messages": [
                            {"text": {"text": ["I'm sorry, I had a little trouble dreaming up a story just now. Could you try asking again?"]}}
                        ]
                    }
                }
            ) # Flask jsonify defaults to HTTP 200 OK

    return app


# ---------------------------------------------------------------------------
# Entrypoint (CLI run, not when imported by WSGI)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    flask_app = create_app()
    # Get port from environment variable or default to 3000
    port = int(os.getenv("PORT", "3000"))
    print(f"🚀 Starting Flask development server on http://0.0.0.0:{port}")
    flask_app.run(host="0.0.0.0", port=port)
