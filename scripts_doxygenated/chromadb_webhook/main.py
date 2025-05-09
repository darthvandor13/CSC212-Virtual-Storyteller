##! @file main.py
##! @brief  Cloud‑function handler that queries ChromaDB for story snippets and returns them to Dialogflow CX.
##!
##! This refactored version separates concerns into small helper functions so that
##! Doxygen can provide rich parameter/return tables while preserving the original
##! behaviour and emoji logging.  Runtime‑critical constants are exposed at the top
##! for easy configuration via environment variables.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT

from __future__ import annotations

import os
import requests
from typing import Dict, List
from flask import Request, jsonify

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHROMA_DB_HOST: str = os.getenv("CHROMA_DB_HOST", "http://34.118.162.201:8000")
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "stories")
CHROMA_TIMEOUT_SEC: int = int(os.getenv("CHROMA_TIMEOUT_SEC", "10"))

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_user_query(payload: Dict) -> str:
    """Extract protagonist, theme, and moral from Dialogflow CX JSON.

    @param payload Raw JSON body sent by Dialogflow CX.
    @return Space‑separated query string. Empty if nothing supplied.
    """
    params = payload.get("sessionInfo", {}).get("parameters", {})
    protagonist = params.get("protagonist", "").strip()
    theme       = params.get("theme", "").strip()
    moral       = params.get("moral", "").strip()
    return " ".join(filter(None, (protagonist, theme, moral)))


def query_chromadb(query: str, n_results: int = 3) -> List[str]:
    """Perform a REST query against ChromaDB.

    @param query       Prepared search string.
    @param n_results   Maximum number of documents to return.
    @return List of document strings (may be empty).
    @throws HTTPError  If the ChromaDB server responds with non‑200.
    """
    response = requests.post(
        f"{CHROMA_DB_HOST}/api/v1/query",
        json={
            "collection_name": COLLECTION_NAME,
            "query_texts": [query],
            "n_results": n_results,
        },
        timeout=CHROMA_TIMEOUT_SEC,
    )
    response.raise_for_status()
    data = response.json()
    docs = data.get("documents", [[]])
    return docs[0] if docs and isinstance(docs[0], list) else []


def make_dialogflow_response(text: str) -> Dict:
    """Wrap plain text in Dialogflow CX fulfillment JSON."""
    return {
        "fulfillment_response": {
            "messages": [{"text": {"text": [text]}}]
        }
    }

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main(request: Request):
    """Google Cloud Functions / Cloud Run entry‑point.

    @param request Flask Request object provided by the platform.
    @return Flask Response (JSON) understood by Dialogflow CX.
    """
    payload = request.get_json(silent=True) or {}
    query_string = parse_user_query(payload)
    print(f"📥 User query: '{query_string}'")

    if not query_string:
        return jsonify(make_dialogflow_response(
            "I didn't catch the hero, theme, or moral. Could you repeat that?"
        ))

    try:
        docs = query_chromadb(query_string, n_results=3)
        if docs:
            reply = "Here are some stories I found: " + ", ".join(docs[:3])
        else:
            reply = "Sorry, I couldn't find any stories that match your request."
    except Exception as exc:
        print(f"❌ ChromaDB error: {exc}")
        reply = "Something went wrong while searching the story database."

    return jsonify({"story_snippet": reply})

# ---------------------------------------------------------------------------
# Local dev server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from flask import Flask, request as _req

    flask_app = Flask(__name__)

    @flask_app.post("/query")
    def _local_query():
        return main(_req)

    flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")), debug=True)

