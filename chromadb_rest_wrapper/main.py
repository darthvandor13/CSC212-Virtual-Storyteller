from fastapi import FastAPI
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
async def query_chromadb(request: QueryRequest):
    try:
        print(f"📥 Received query: {request.query}")
        results = collection.query(query_texts=[request.query], n_results=3)
        docs = results.get("documents", [[]])[0]

        # Format the message to send back to the Conversational Agent
        response_text = "\n\n".join(docs)

        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        }

    except Exception as e:
        print(f"❌ Error during query: {e}")
        return {
            "fulfillment_response": {
                "messages": [
                    {
                        "text": {
                            "text": ["Sorry, something went wrong with the story search."]
                        }
                    }
                ]
            }
        }
