import requests
from flask import jsonify, Request

CHROMA_DB_HOST = "http://34.118.162.201:8000"
COLLECTION_NAME = "stories"

def main(request: Request):
    req = request.get_json()
    user_query = req.get('queryResult', {}).get('queryText', '')
    print(f"📥 Received query: {user_query}")

    try:
        # Send query to ChromaDB HTTP API
        response = requests.post(
            f"{CHROMA_DB_HOST}/api/v1/query",
            json={
                "collection_name": COLLECTION_NAME,
                "query_texts": [user_query],
                "n_results": 3
            },
            timeout=10
        )

        print(f"🌐 Response status: {response.status_code}")
        print(f"📦 Response JSON: {response.text}")

        if response.status_code != 200:
            raise Exception("ChromaDB query failed.")

        result = response.json()
        documents = result.get("documents", [[]])

        if not documents or not documents[0]:
            response_text = "Sorry, I couldn't find any stories that match your request."
        else:
            top_docs = documents[0]
            response_text = "Here are some stories: " + ", ".join(top_docs[:3])

    except Exception as e:
        print(f"❌ Error during query: {e}")
        response_text = "Something went wrong while searching stories."

    return jsonify({"fulfillmentText": response_text})

