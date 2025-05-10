#!/usr/bin/env python3
import chromadb

# Connect using PersistentClient (on the VM)
client = chromadb.PersistentClient(path="/home/cvandor/chroma_db")

collections = client.list_collections()
print(f"💾 Collections stored locally: {collections}")

MAX_TITLES = 25  # Max number of unique titles to display
MAX_PEEK = 5000   # How many chunks to peek at (must be >= MAX_TITLES)

for name in collections:
    print(f"\n📚 Collection: {name}")
    collection = client.get_collection(name)

    try:
        total_chunks = collection.count()
        peek = collection.peek(limit=MAX_PEEK)
        print(f"   🔢 Total chunks: {total_chunks}")

        seen_titles = set()
        print(f"   📖 Sample unique story titles (up to {MAX_TITLES}):")

        for metadata in peek["metadatas"]:
            title = metadata.get("title", "Unknown").strip()
            if title and title.lower() not in seen_titles:
                print(f"      - {title}")
                seen_titles.add(title.lower())
                if len(seen_titles) >= MAX_TITLES:
                    break

        if not seen_titles:
            print("      ⚠️ No titles found in sample metadata.")
    except Exception as e:
        print(f"❌ Error accessing collection '{name}': {e}")
