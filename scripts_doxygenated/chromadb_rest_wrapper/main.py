##! @file main.py
##! @brief  FastAPI wrapper that exposes a /query endpoint to search ChromaDB
##!         for story snippets based on protagonist, theme, and moral.
##!
##! *Refactor rationale*: split startup, parameter‑parsing, query, and error
##! handling into dedicated functions so Doxygen can provide granular API docs
##! and call graphs while preserving behaviour and emoji logging.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT License
##!

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import chromadb
import os
import sys
from typing import Dict, Any, Optional

__all__ = [
    "QueryRequest",
    "create_chroma_collection",
    "build_query_string",
    "search_stories",
    "format_dialogflow_error",
    "app",
]

# ---------------------------------------------------------------------------
# Configuration constants (could be env‑driven)                               
# ---------------------------------------------------------------------------

CHROMA_HOST: str = os.getenv("CHROMA_HOST", "34.118.162.201")
CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "stories")

# ---------------------------------------------------------------------------
# Helper / init                                                               
# ---------------------------------------------------------------------------

def create_chroma_collection(host: str, port: int, name: str):
    """Attempt to connect to ChromaDB and return the collection object.

    Raises
    ------
    RuntimeError
        If the connection or collection retrieval fails.
    """
    try:
        client = chromadb.HttpClient(host=host, port=port)
        return client.get_collection(name)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to connect to ChromaDB {host}:{port} or get collection '{name}'."
        ) from exc


def build_query_string(protagonist: str, theme: str, moral: str) -> str:
    """Concatenate parameters into a single search string (trim whitespace)."""
    return f"{protagonist} {theme} {moral}".strip()


def search_stories(collection, query: str, n_results: int = 3) -> str:
    """Query ChromaDB and return a merged snippet or fallback message."""
    if not query:
        return "It seems the details for the story were unclear. Let's try again!"

    results: Dict[str, Any] = collection.query(query_texts=[query], n_results=n_results)
    documents = results.get("documents", [])

    if documents and isinstance(documents[0], list):
        return "\n\n".join(documents[0])
    return "I searched the archives, but couldn't find anything matching that specific combination."


def format_dialogflow_error(message: str) -> Dict[str, Any]:
    """Return an error payload formatted for Dialogflow CX."""
    return {
        "fulfillment_response": {
            "messages": [{"text": {"text": [message]}}]
        }
    }

# ---------------------------------------------------------------------------
# FastAPI setup                                                               
# ---------------------------------------------------------------------------

app = FastAPI()

try:
    COLLECTION = create_chroma_collection(CHROMA_HOST, CHROMA_PORT, COLLECTION_NAME)
    print(
        f"Successfully connected to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT} "
        f"and retrieved '{COLLECTION_NAME}'"
    )
except RuntimeError as err:
    print(f"❌ CRITICAL: {err}", file=sys.stderr)
    COLLECTION = None  # Allows startup; requests will handle the error.


class QueryRequest(BaseModel):
    query: Optional[str] = ""


@app.post("/query")
async def query_endpoint(req: Request):
    payload = await req.json()
    print(f"Received payload: {payload}")

    if COLLECTION is None:
        return format_dialogflow_error("Sorry, the story database is currently unavailable.")

    try:
        params = payload.get("sessionInfo", {}).get("parameters", {})
        protagonist = params.get("protagonist", "")
        theme = params.get("theme", "")
        moral = params.get("moral", "")

        query_str = build_query_string(protagonist, theme, moral)
        print(f"📥 Query string: '{query_str}'")

        snippet = search_stories(COLLECTION, query_str)
        print(f"📝 Snippet preview: '{snippet[:200]}…'")

        return {"story_snippet": snippet}

    except Exception as exc:
        print(f"❌ Error processing request: {exc}", file=sys.stderr)
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# Dev‑only launcher ----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)), reload=True)

