##! @file webhook.py
##! @brief  Dialogflow CX fulfilment webhook that generates an interactive
##!         short story with OpenAI ChatCompletion.
##!
##! This version is reorganised into small, reusable functions so that
##! Doxygen can render clear parameter / return tables and call graphs while
##! preserving the original runtime behaviour.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT License
##!
##! ### Environment variables
##! * **OPENAI_API_KEY** — secret API key for the ChatCompletion endpoint.
##!
##! ### Flask routes
##! * **POST /webhook** — primary Dialogflow CX fulfilment entry‑point.
##!
##! ---

from __future__ import annotations

import os
from typing import Dict, Any

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import openai

load_dotenv()

#: OpenAI API secret (read once at import time)
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY  # type: ignore

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def build_prompt(username: str, theme: str, moral: str) -> str:
    """Craft the instructional prompt sent to ChatGPT.

    @param username: Recipient of the story (default *Adventurer*).
    @param theme:    Story genre / setting (e.g., *fantasy*, *sci‑fi*).
    @param moral:    Core lesson to convey (e.g., *courage*).
    @return Prompt string ready for ChatCompletion.
    """
    return (
        f"Create a short interactive story for {username} in a {theme} setting, "
        f"where the story teaches a lesson about {moral}. Make it engaging and immersive."
    )


def call_chatgpt(prompt: str) -> str:
    """Send the prompt to OpenAI and return the model's reply.

    @param prompt: Fully‑formed prompt as returned by :pyfunc:`build_prompt`.
    @raises openai.OpenAIError: If the HTTP request fails.
    @return The assistant's textual response.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]  # type: ignore[index]


# ---------------------------------------------------------------------------
# Flask setup
# ---------------------------------------------------------------------------

def create_app() -> Flask:
    """Factory that builds and returns the Flask application object."""

    app = Flask(__name__)

    @app.route("/webhook", methods=["POST"])
    def webhook_endpoint() -> Any:  # noqa: ANN401  (Flask requires Any return)
        """Dialogflow CX fulfilment route (expects JSON body)."""
        try:
            body: Dict[str, Any] = request.get_json(force=True)
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
        except Exception as exc:  # pragma: no cover — broad catch matches legacy behaviour
            print("Webhook error:", exc)
            return (
                jsonify(
                    {
                        "fulfillment_response": {
                            "messages": [
                                {"text": {"text": ["Error processing request."]}}
                            ]
                        }
                    }
                ),
                500,
            )

    return app


# ---------------------------------------------------------------------------
# Entrypoint (CLI run, not when imported by WSGI)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=3000)

