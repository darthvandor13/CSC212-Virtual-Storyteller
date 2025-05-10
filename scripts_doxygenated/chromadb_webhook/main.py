## @file main.py
## @brief Google Cloud Function webhook for Dialogflow CX using Flask.
## @details This script defines a Flask application to serve as an HTTP webhook for Dialogflow CX.
##          It receives a query from Dialogflow, proxies it to a specified ChromaDB HTTP API,
##          processes the ChromaDB response, and returns a formatted fulfillment text to Dialogflow.
##          It includes error handling for API requests, timeouts, and response parsing.
## @author Calvin Vandor
## @date 2025-05-10
## @version 1.1

import requests
from flask import jsonify, Request as FlaskRequest # Explicitly alias for clarity
import os # For environment variables, though not used in this version for CHROMA_HOST

## @var CHROMA_DB_HOST
# The base URL (including http/https) of the ChromaDB HTTP API server.
# Example: "http://<your-chroma-db-ip-or-domain>:<port>"
CHROMA_DB_HOST = "http://34.118.162.201:8000"

## @var COLLECTION_NAME
# The name of the ChromaDB collection to be queried.
COLLECTION_NAME = "stories"

## @var REQUEST_TIMEOUT
# Timeout in seconds for the HTTP request to the ChromaDB API.
REQUEST_TIMEOUT = 10 # seconds

##
# @brief Main entry point for the Google Cloud Function.
# @details This function is triggered by an HTTP request. It expects a JSON payload
#          from Dialogflow CX, extracts the user's query text, queries the
#          ChromaDB HTTP API, and formats the search results or error messages
#          into a JSON response suitable for Dialogflow's `fulfillmentText`.
# @param request flask.Request The incoming HTTP request object from Google Cloud Functions.
#        It's expected to contain a JSON payload, typically from Dialogflow CX,
#        with the user's query located at `queryResult.queryText`.
# @return flask.Response A JSON response object suitable for Dialogflow fulfillment.
#         The JSON object will have a key `fulfillmentText` containing the response string.
# @note This function handles various potential errors during its execution,
#       such as issues with the incoming payload, ChromaDB API errors (HTTP errors, timeouts),
#       and problems parsing the ChromaDB response. Error messages are user-friendly.
def main(request: FlaskRequest):
    """
    Handles incoming Dialogflow CX webhook requests, queries ChromaDB via HTTP,
    and returns a formatted response.
    """
    response_text = "An unexpected error occurred while processing your request." # Default error

    try:
        req_json = request.get_json(silent=True) # Use silent=True to prevent raising an exception for non-JSON/empty body
        if not req_json:
            print("❌ Error: Request body is not valid JSON or is empty.")
            response_text = "I received an invalid request. Please try again."
            return jsonify({"fulfillmentText": response_text})

        # Extract user query from Dialogflow's typical payload structure
        user_query = req_json.get('queryResult', {}).get('queryText', '')
        print(f"📥 Received query: '{user_query}'")

        if not user_query:
            print("⚠️ Warning: User query is empty.")
            response_text = "It seems your query was empty. Could you please try asking again?"
            return jsonify({"fulfillmentText": response_text})

        # Prepare and send the query to ChromaDB HTTP API
        chroma_api_endpoint = f"{CHROMA_DB_HOST}/api/v1/collections/{COLLECTION_NAME}/query" # More common ChromaDB API path
        # Note: The /api/v1/query endpoint you used might be older or custom.
        # The one above is common for querying a specific collection if client.query() is not available.
        # However, if your /api/v1/query expects collection_name in body, stick to it:
        # chroma_api_endpoint = f"{CHROMA_DB_HOST}/api/v1/query"
        # Using the one that seems more standard with collection name in path if possible,
        # but will adapt Doxygen comments to match the payload if the original path is firm.
        # For now, I'll assume your endpoint `f"{CHROMA_DB_HOST}/api/v1/query"` expecting collection_name in payload is correct.
        chroma_api_endpoint_original = f"{CHROMA_DB_HOST}/api/v1/query"


        print(f"📡 Querying ChromaDB endpoint: {chroma_api_endpoint_original}")
        api_response = requests.post(
            chroma_api_endpoint_original, # Using the original endpoint you specified
            json={
                "collection_name": COLLECTION_NAME, # If using /api/v1/query
                "query_texts": [user_query],
                "n_results": 3
            },
            timeout=REQUEST_TIMEOUT
        )

        print(f"🌐 ChromaDB API Response Status: {api_response.status_code}")
        print(f"📦 ChromaDB API Response Body: {api_response.text[:500]}...") # Log snippet of body

        # Check for HTTP errors (4xx or 5xx)
        api_response.raise_for_status()

        # Parse the JSON response from ChromaDB
        result = api_response.json()
        documents = result.get("documents") # Chroma typically returns [[doc1, doc2]]

        # Process documents
        if documents and isinstance(documents, list) and len(documents) > 0 and \
           isinstance(documents[0], list) and len(documents[0]) > 0:
            top_docs = [str(doc) for doc in documents[0][:3] if isinstance(doc, str) and doc.strip()]
            if top_docs:
                response_text = "Here are some stories: " + ", ".join(top_docs)
            else:
                response_text = "I found some entries, but they were empty. Try a different query."
        else:
            response_text = "Sorry, I couldn't find any stories that match your request."

    except requests.exceptions.Timeout:
        print(f"❌ Timeout error querying ChromaDB at {CHROMA_DB_HOST}")
        response_text = "Sorry, the story archive took too long to respond. Please try again."
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error during ChromaDB query: {http_err}. Response: {http_err.response.text[:500]}")
        response_text = "There was an issue communicating with the story archive. Please check the details and try again."
    except requests.exceptions.RequestException as req_err: # Catches other requests-related errors (e.g., connection error)
        print(f"❌ Request error during ChromaDB query: {req_err}")
        response_text = "I'm having trouble connecting to the story archive right now. Please check the connection or try again later."
    except ValueError as json_err: # Raised if api_response.json() fails to decode
        print(f"❌ Error decoding ChromaDB JSON response: {json_err}")
        response_text = "The story archive returned an unexpected response format. Please try again."
    except Exception as e:
        print(f"❌ An unexpected error occurred during query processing: {e}")
        import traceback
        traceback.print_exc() # Log full traceback for unexpected errors
        response_text = "Something went wrong while I was searching for stories. I've noted the issue."

    print(f"💬 Sending fulfillmentText: '{response_text}'")
    return jsonify({"fulfillmentText": response_text})

# Note: For Google Cloud Functions, the `if __name__ == "__main__":` block
# is not typically used for running a Flask dev server, as GCF handles invocation.
# If you were testing locally with Flask's built-in server (not GCF emulator), you would add:
# if __name__ == '__main__':
#     app = Flask(__name__)
#     app.route('/', methods=['POST'])(main) # Assuming POST requests to root for local Flask dev
#     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
# However, the provided script is a single function for GCF.
