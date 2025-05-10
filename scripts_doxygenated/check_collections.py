## @file check_collections.py
# @brief Script to inspect a specific ChromaDB collection named "stories".
# @details This script connects to a local persistent ChromaDB instance,
#          retrieves the "stories" collection, counts the number of chunks
#          (vector embeddings), and displays a sample of their metadata.
#          This version is for the script that focuses on the "stories" collection.
# @author Calvin Vandor
# @date 2025-05-10

import chromadb

## @brief Main execution block of the script.
# @details Connects to ChromaDB, accesses the "stories" collection,
#          and prints its size and a sample of its metadata.
def main():
    """
    Connects to ChromaDB, retrieves the 'stories' collection,
    counts its items, and peeks at its metadata.
    """
    try:
        # Connect to the local persistent ChromaDB instance
        # @var chroma_client
        #      The ChromaDB persistent client object.
        chroma_client = chromadb.PersistentClient(path="/home/cvandor/chroma_db")

        # Get the specific collection "stories"
        # @var vector_store
        #      The "stories" collection object.
        vector_store = chroma_client.get_collection("stories")

        # Safely count and peek at the collection
        ## @var total_chunks
        #      The total number of chunks in the "stories" collection.
        total_chunks = vector_store.count()
        ## @var peek
        #      A dictionary containing a sample of up to 10 items from the "stories" collection.
        peek = vector_store.peek(limit=10)

        print(f"🔎 Total chunks in 'stories': {total_chunks}")

        if peek and peek.get("metadatas"): # Ensure 'peek' is not None and 'metadatas' key exists
            print("📌 Sample metadata:")
            for metadata in peek["metadatas"]:
                print(f"    - {metadata}")
        elif total_chunks == 0:
            print("ℹ️ The 'stories' collection is empty. No metadata to display.")
        else:
            print("⚠️ No metadata found in the sample, or the sample was empty.")

    except chromadb.errors.CollectionNotFoundError:
        print(f"❌ Error: The collection 'stories' was not found. Please ensure it exists.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
