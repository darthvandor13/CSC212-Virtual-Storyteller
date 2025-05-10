#!/usr/bin/env python3
import chromadb

# Connect to the local persistent ChromaDB instance
chroma_client = chromadb.PersistentClient(path="/home/cvandor/chroma_db")
vector_store = chroma_client.get_collection("stories")

# Safely count and peek at the collection
try:
    total_chunks = vector_store.count()
    peek = vector_store.peek(limit=10)

    print(f"🔎 Total chunks in 'stories': {total_chunks}")
    if peek["metadatas"]:
        print("📌 Sample metadata:")
        for metadata in peek["metadatas"]:
            print(f"   - {metadata}")
    else:
        print("⚠️ No metadata found. The database might still be empty.")
except Exception as e:
    print(f"❌ Error checking collection: {e}")
