##! @file chatgpt_webhook.py
##! @brief  Flask webhook that turns a single keyword into a children’s story
##!         using the OpenAI ChatCompletion API.
##!
##! This refactor wraps the global Flask instance and the OpenAI logic in small,
##! documented helper functions so that Doxygen can export a neat API reference
##! (parameter tables, call‑graphs).  Runtime behaviour is **identical** to the
##! legacy script — just `python chatgpt_webhook.py` to run a local server on
##! port 5000.
##!
##! @author   Calvin Vandor
##! @date     2025‑05‑08
##! @copyright MIT License
##!
##! ### Environment variables
##! * **AI_STORYTELLER_TEST_KEY_CV** – your OpenAI API key (secret)
##!
##! ### Example (curl)
##! ```bash
##! curl -X POST http://localhost:5000/generate_story \
##!      -H "Content-Type: application/json" \
##!      -d '{"word": "dragon"}'
##! ```
##! returns `{ "story": "Once upon a time…" }`
##!

from __future__ import annotations

import os
import requests
from flask import Flask, jsonify, request
from typing import Dict, Any

__all__ = ["create_app", "generate_story"]


#: OpenAI endpoint used by :pyfunc:`generate_story`.
_OPENAI_URL: str = "https://api.openai.com/v1/chat/completions"


def _openai_headers(api_key: str) -> Dict[str, str]:
    """Return HTTP headers for the ChatCompletion request.

    @param api_key: Secret key from the environment variable.
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def generate_story(keyword: str, *, api_key: str | None = None, model: str = "gpt-4o-mini") -> str:
    """Call OpenAI and return a short children’s story.

    @param keyword:        Topic or noun the user spoke (e.g. "robot").
    @param api_key:        Optional override for the *AI_STORYTELLER_TEST_KEY_CV* env‑var.
    @param model:          ChatCompletion model (default ``gpt-4o-mini``).
    @return:               Story text or an error message.
    """
    api_key = api_key or os.getenv("AI_STORYTELLER_TEST_KEY_CV", "")
    if not api_key:
        return "Error: API key not set."

    body: Dict[str, Any] = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": f"Tell a short children's story about {keyword}",
            }
        ],
    }

    resp = requests.post(_OPENAI_URL, headers=_openai_headers(api_key), json=body, timeout=30)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]

    return f"Error {resp.status_code}: Unable to generate story."


def create_app() -> Flask:
    """Factory that creates and configures the Flask application instance."""

    app = Flask(__name__)

    @app.route("/generate_story", methods=["POST"])
    def webhook():  # noqa: D401
        """POST /generate_story → JSON { "story": … }.

        Expected payload::

            { "word": "dragon" }
        """
        data = request.get_json(force=True, silent=True) or {}
        keyword = data.get("word", "an adventure")
        story = generate_story(keyword)
        return jsonify({"story": story})

    return app


if __name__ == "__main__":
    # Stand‑alone launch: `python chatgpt_webhook.py`
    create_app().run(host="0.0.0.0", port=5000)

