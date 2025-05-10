##! @file main_merged.py
##! @brief FastAPI wrapper for ChromaDB story search, optimized for Dialogflow CX.
##! @details
##! This application provides a /query endpoint that interfaces with ChromaDB
##! to find story snippets based on protagonist, theme, and moral provided
##! in a Dialogflow CX webhook request. It emphasizes robust error handling,
##! consistent Dialogflow-formatted responses, and flexible configuration
##! through environment variables.
##!
##! Key features:
##! - FastAPI for asynchronous request handling.
##! - Pydantic models for request validation.
##! - ChromaDB client for vector search.
##! - Modular design with helper functions for clarity and testability.
##! - Configuration via environment variables.
##! - Consistent JSON response formatting for Dialogflow CX.
##!
##! @author Calvin Vandor
##! @date   2025-05-10
##! @version 1.1
##! @copyright MIT License

import chromadb
import os
import sys
from typing import List, Dict, Any, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# --- Module Exports ---
__all__ = [
    "DialogflowParameters",
    "DialogflowSessionInfo",
    "DialogflowWebhookRequest",
    "create_chroma_collection",
    "build_query_string",
    "search_stories",
    "format_dialogflow_error_response",
    "app",
    "query_endpoint",
    "COLLECTION"
]

# --- Configuration Constants ---
# Loaded from environment variables with defaults
CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost") # Defaulted for easier local dev
CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "stories")
DEFAULT_N_RESULTS: int = int(os.getenv("DEFAULT_N_RESULTS", "3"))

# --- Pydantic Models for Dialogflow Webhook Request ---

class DialogflowParameters(BaseModel):
    """Pydantic model for parameters within Dialogflow sessionInfo."""
    protagonist: Optional[str] = Field(default="", description="The protagonist of the story.")
    theme: Optional[str] = Field(default="", description="The main theme of the story.")
    moral: Optional[str] = Field(default="", description="The moral or lesson of the story.")

class DialogflowSessionInfo(BaseModel):
    """Pydantic model for Dialogflow sessionInfo."""
    parameters: DialogflowParameters = Field(default_factory=DialogflowParameters)

class DialogflowWebhookRequest(BaseModel):
    """Pydantic model for the incoming Dialogflow webhook request."""
    sessionInfo: DialogflowSessionInfo = Field(default_factory=DialogflowSessionInfo)
    # Add other Dialogflow fields if needed, e.g., fulfillmentInfo.tag, messages, etc.

# --- ChromaDB and Helper Functions ---

## @var COLLECTION
# Global variable to hold the ChromaDB collection object.
# Initialized at application startup.
COLLECTION: Optional[chromadb.api.models.Collection.Collection] = None

def create_chroma_collection(host: str, port: int, name: str) -> Optional[chromadb.api.models.Collection.Collection]:
    """
    Attempts to connect to ChromaDB and retrieve the specified collection.

    @param host The hostname or IP address of the ChromaDB server.
    @param port The port number of the ChromaDB server.
    @param name The name of the collection to retrieve.
    @return The ChromaDB collection object if successful, None otherwise.
    """
    try:
        print(f"Attempting to connect to ChromaDB at {host}:{port}...")
        client = chromadb.HttpClient(host=host, port=port)
        # You might want to add a client.heartbeat() or similar check if your ChromaDB version supports it
        print(f"Successfully created ChromaDB client. Getting collection '{name}'...")
        collection = client.get_collection(name)
        print(f"Successfully retrieved collection '{name}'.")
        return collection
    except Exception as e:
        print(f"❌ Error connecting to ChromaDB or getting collection '{name}': {e}", file=sys.stderr)
        return None

def build_query_string(protagonist: str, theme: str, moral: str) -> str:
    """
    Concatenates protagonist, theme, and moral into a single search string.
    Only non-empty parts are joined. Whitespace is trimmed.

    @param protagonist The protagonist of the story.
    @param theme The main theme of the story.
    @param moral The moral or lesson of the story.
    @return A concatenated query string.
    """
    query_parts = []
    if protagonist and protagonist.strip(): query_parts.append(protagonist.strip())
    if theme and theme.strip(): query_parts.append(theme.strip())
    if moral and moral.strip(): query_parts.append(moral.strip())
    return " ".join(query_parts) # No need to strip here if parts are already stripped

def search_stories(collection: chromadb.api.models.Collection.Collection, query: str, n_results: int = DEFAULT_N_RESULTS) -> str:
    """
    Queries the ChromaDB collection and returns a merged snippet of story documents
    or a user-facing fallback message if no relevant stories are found or an error occurs.

    @param collection The ChromaDB collection object to query.
    @param query The query string to search for.
    @param n_results The number of results to retrieve from ChromaDB.
    @return A string containing merged story snippets or a user-facing fallback/error message.
    """
    if not query: # Query effectively empty after build_query_string
        print("⚠️ Query string is empty. Returning fallback message.")
        return "It seems the details for the story were unclear. Could you please provide more information?"

    try:
        print(f"Querying ChromaDB collection with text: '{query}', n_results: {n_results}")
        results: Dict[str, Any] = collection.query(query_texts=[query], n_results=n_results)
        print(f"ChromaDB query raw results: {results}")

        documents = results.get("documents")

        if documents and isinstance(documents, list) and len(documents) > 0:
            first_query_results = documents[0] # ChromaDB returns a list of lists for documents
            if isinstance(first_query_results, list) and len(first_query_results) > 0:
                valid_snippets = [doc for doc in first_query_results if isinstance(doc, str) and doc.strip()]
                if valid_snippets:
                    return "\n\n".join(valid_snippets)
                else:
                    print("⚠️ Documents list was present but contained no valid (non-empty string) snippets.")
            elif isinstance(first_query_results, list) and len(first_query_results) == 0:
                 print("⚠️ Documents list for the first query was empty.")
            else:
                print(f"⚠️ Expected list of documents for the first query, but got: {type(first_query_results)}")
        else:
            print("⚠️ No documents found or 'documents' key missing/empty/invalid in ChromaDB results.")

        return "I searched the archives, but couldn't find anything matching that specific combination of details."
    except Exception as e:
        print(f"❌ Error during ChromaDB query or processing results: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return "I encountered an unexpected issue while searching the story archives. Please try again."


def format_dialogflow_error_response(message: str) -> Dict[str, Any]:
    """
    Formats an error message into the JSON structure expected by Dialogflow CX
    for a fulfillment response.

    @param message The error message text to be sent to the user.
    @return A dictionary representing the Dialogflow CX error response.
    """
    return {
        "fulfillment_response": {
            "messages": [{"text": {"text": [message]}}]
        }
    }

# --- FastAPI Application Setup ---

app = FastAPI(
    title="ChromaDB Story Search API for Dialogflow",
    description="Exposes an endpoint to search for story snippets in ChromaDB based on Dialogflow parameters.",
    version="1.1.0" # Incremented version
)

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Initializes the connection to ChromaDB and retrieves the collection.
    """
    global COLLECTION
    print("FastAPI application starting up...")
    COLLECTION = create_chroma_collection(CHROMA_HOST, CHROMA_PORT, COLLECTION_NAME)
    if COLLECTION:
        print(f"✅ ChromaDB collection '{COLLECTION_NAME}' initialized and ready.")
    else:
        print(f"⚠️ CRITICAL WARNING: ChromaDB collection '{COLLECTION_NAME}' could NOT be initialized. The API will report errors for all queries.")

@app.post("/query")
async def query_endpoint(request: DialogflowWebhookRequest):
    """
    Handles POST requests to the /query endpoint.
    Extracts story parameters from the Dialogflow webhook request (parsed by Pydantic),
    queries ChromaDB, and returns a story snippet or an error message
    formatted for Dialogflow CX.

    @param request The incoming Dialogflow webhook request.
    @return A JSON response suitable for Dialogflow CX.
    """
    # Pydantic model_dump_json is useful for complete, pretty-printed request logging
    print(f"Received request payload: {request.model_dump_json(indent=2)}")

    if COLLECTION is None:
        print("❌ Error: ChromaDB collection is not available (failed at startup).", file=sys.stderr)
        return JSONResponse(
            status_code=200, # Dialogflow often expects 200 OK for functional errors in payload
            content=format_dialogflow_error_response(
                "I'm sorry, but the story database is currently unavailable. Please try again later."
            )
        )

    try:
        params = request.sessionInfo.parameters # Pydantic ensures sessionInfo and parameters exist due to default_factory
        protagonist = params.protagonist
        theme = params.theme
        moral = params.moral

        print(f"Extracted parameters - Protagonist: '{protagonist}', Theme: '{theme}', Moral: '{moral}'")

        query_str = build_query_string(protagonist, theme, moral)
        print(f"📥 Constructed query string for ChromaDB: '{query_str}'")

        # search_stories now returns a user-facing message if the query_str is empty,
        # if no results are found, or if an internal error occurred during search.
        snippet_or_message = search_stories(COLLECTION, query_str, n_results=DEFAULT_N_RESULTS)
        print(f"📝 Result from search_stories: '{snippet_or_message[:300]}...'")

        # Check if the result from search_stories is one of the predefined fallback/error messages.
        user_facing_error_messages = [
            "It seems the details for the story were unclear. Could you please provide more information?",
            "I searched the archives, but couldn't find anything matching that specific combination of details.",
            "I encountered an unexpected issue while searching the story archives. Please try again."
        ]

        if snippet_or_message in user_facing_error_messages:
            return JSONResponse(
                status_code=200,
                content=format_dialogflow_error_response(snippet_or_message)
            )
        else:
            # Success: return the story snippet directly.
            # This format implies setting an output parameter or similar in Dialogflow.
            return {"story_snippet": snippet_or_message}

    except Exception as e:
        # Catch-all for any other unexpected errors during request processing logic in this endpoint
        print(f"❌ Unexpected error processing request in /query endpoint: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=200, # Consistent 200 OK for Dialogflow with error in body
            content=format_dialogflow_error_response(
                "I'm terribly sorry, but a mysterious gremlin seems to have tinkered with my scrolls! Please try asking again."
            )
        )

# --- Uvicorn Runner for Local Development ---
if __name__ == "__main__":
    import uvicorn
    server_port = int(os.getenv("PORT", "8080")) # Common for cloud environments
    print(f"Starting Uvicorn development server on http://0.0.0.0:{server_port}")
    uvicorn.run(
        "main_merged:app", # Make sure your file is named main_merged.py
        host="0.0.0.0",
        port=server_port,
        reload=True # Useful for development; consider removing for production
    )
