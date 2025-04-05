from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import chromadb

app = FastAPI()

# ChromaDB setup
chroma_client = chromadb.HttpClient(host="34.118.162.201", port=8000)
collection = chroma_client.get_collection("stories")

# Request model
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_endpoint(request: Request):
    payload = await request.json()

    # Extract parameters from the webhook request
    try:
        protagonist = payload["sessionInfo"]["parameters"].get("protagonist", "")
        theme = payload["sessionInfo"]["parameters"].get("theme", "")
        moral = payload["sessionInfo"]["parameters"].get("moral", "")
    except Exception as e:
        return JSONResponse(
            content={"fulfillment_response": {"messages": [{"text": {"text": [f"Error parsing input: {str(e)}"]}}]}},
            status_code=400
        )

    query_string = f"{protagonist} {theme} {moral}"
    print(f"📥 Received query: {query_string}")

    try:
        results = collection.query(query_texts=[query_string], n_results=3)
        documents = results.get("documents", [[""]])[0]
        merged_text = "\n\n".join(documents)

        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [merged_text]
                        }
                    }
                ]
            }
        }
    except Exception as e:
        print(f"❌ Error querying ChromaDB: {e}")
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [f"Sorry, something went wrong with the story search. ({str(e)})"]
                        }
                    }
                ]
            }
        }
