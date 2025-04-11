from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import chromadb
import sys # Added for potentially more detailed error printing

app = FastAPI()

# ChromaDB setup
# Ensure these are correct for your setup
CHROMA_HOST = "34.118.162.201"
CHROMA_PORT = 8000
COLLECTION_NAME = "stories"

try:
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    # Optional: Add a heartbeat check if supported by your ChromaDB version/client
    # chroma_client.heartbeat() # Uncomment if applicable and needed
    collection = chroma_client.get_collection(COLLECTION_NAME)
    print(f"Successfully connected to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT} and got collection '{COLLECTION_NAME}'")
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to connect to ChromaDB or get collection '{COLLECTION_NAME}'. Error: {e}", file=sys.stderr)
    # Depending on deployment, you might want the app to fail startup here
    # For now, we'll let requests fail later if collection is None
    collection = None

# Request model - Unused in this version but good practice
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: Request):
    payload = await request.json()
    print(f"Received request payload: {payload}") # Log entire payload for debugging

    # Check if ChromaDB connection was successful during startup
    if collection is None:
        print("❌ Error: ChromaDB collection is not available.", file=sys.stderr)
        # Return an error structure Dialogflow understands
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["Sorry, the story database is currently unavailable."]
                        }
                    }
                ]
            }
        }

    # Extract parameters from the webhook request
    try:
        # Ensure sessionInfo and parameters exist before accessing
        session_info = payload.get("sessionInfo", {})
        parameters = session_info.get("parameters", {})

        protagonist = parameters.get("protagonist", "")
        theme = parameters.get("theme", "")
        moral = parameters.get("moral", "")

        print(f"Extracted parameters - Protagonist: '{protagonist}', Theme: '{theme}', Moral: '{moral}'")

        if not protagonist and not theme and not moral:
             print("⚠️ Warning: All parameters (protagonist, theme, moral) are empty.")
             # Decide if you want to proceed or return an error/default

    except Exception as e:
        print(f"❌ Error parsing input parameters: {e}", file=sys.stderr)
        # Using JSONResponse to explicitly set status code
        return JSONResponse(
            status_code=400,
            content={
                "fulfillment_response": {
                    "messages": [{"text": {"text": [f"Error parsing input: {str(e)}"]}}]
                }
            }
        )

    # Avoid querying if essential parameters are missing (optional, adjust as needed)
    if not protagonist and not theme and not moral:
         return {
             "fulfillment_response": {
                 "messages": [{"text": {"text": ["It seems I didn't catch the hero, theme, or moral. Could you tell me again?"]}}]
            }
         }

    query_string = f"{protagonist} {theme} {moral}".strip() # Use strip() to handle cases where some are empty
    print(f"📥 Constructed query string for ChromaDB: '{query_string}'")

    try:
        # Ensure query_string is not empty before querying
        if not query_string:
             print("⚠️ Warning: Query string is empty, returning default message.")
             merged_text = "It seems the details for the story were unclear. Let's try again!"
        else:
            results = collection.query(query_texts=[query_string], n_results=3)
            print(f"ChromaDB query results: {results}") # Log ChromaDB results

            documents = results.get("documents")
            # Handle cases where 'documents' might be None or not in the expected format
            if documents and isinstance(documents, list) and len(documents) > 0:
                first_result_list = documents[0]
                if isinstance(first_result_list, list):
                     merged_text = "\n\n".join(first_result_list)
                else:
                     print(f"⚠️ Warning: Expected list of lists for documents, but got different structure in first element: {type(first_result_list)}")
                     merged_text = "Found some inspiration, but couldn't format it properly."
            else:
                print("⚠️ Warning: No documents found or unexpected format in ChromaDB results.")
                merged_text = "I searched the archives, but couldn't find anything matching that specific combination."

        print(f"📝 Merged text snippet: '{merged_text[:200]}...'") # Log snippet of merged text

        # *** MODIFIED RETURN STATEMENT FOR SUCCESS ***
        return {"story_snippet": merged_text}

    except Exception as e:
        print(f"❌ Error querying ChromaDB or processing results: {e}", file=sys.stderr)
        # Log the full traceback for internal debugging if needed
        import traceback
        traceback.print_exc()

        # Return an error structure Dialogflow understands
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Sorry, something went wrong while searching for the story inspiration. ({str(e)})"]
                        }
                    }
                ]
            }
        }

# Include logic to run with uvicorn if executed directly (for local testing)
if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable if available (common for Cloud Run), otherwise default to 8080
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True) # reload=True is useful for local dev
