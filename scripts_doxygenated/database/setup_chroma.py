##! @file setup_chroma.py
##! @brief  Bulk‑embed local story text files into a ChromaDB collection with
##!         rich metadata (title, author, year, genre, subgenre).
##!
##! _Refactored for Doxygen:_ the original top‑level loop is decomposed into
##! helper functions so Doxygen can produce clear parameter / return tables and
##! call graphs. Runtime behaviour and emoji markers remain unchanged.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT License
##!

import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------

#: Name of the Chroma collection that holds story chunks
COLLECTION_NAME: str = "stories"

#: Local folder where the persistent Chroma DB lives
PERSIST_DIR: str = "./chroma_db"

#: Folder containing plain‑text stories
STORIES_DIR: str = os.path.join(os.path.dirname(__file__), "stories")

# ---------------------------------------------------------------------------
# Initialisation helpers
# ---------------------------------------------------------------------------

def get_openai_key() -> str:
    """Fetch **OPENAI_API_KEY** from environment or raise."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("❌ OpenAI API key is missing. Set it as an environment variable.")
    return key


def init_vector_store(api_key: str) -> Chroma:
    """Create (or open) a persistent Chroma vector store.

    @param api_key: Valid OpenAI API key for embeddings.
    @return:        Ready‑to‑use :class:`Chroma` instance.
    """
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=OpenAIEmbeddings(openai_api_key=api_key),
        persist_directory=PERSIST_DIR,
    )

# ---------------------------------------------------------------------------
# Story processing utilities
# ---------------------------------------------------------------------------

def parse_metadata(filename: str):
    """Extract *author, title, year, genre, subgenre* from a formatted filename.
    Falls back to "Unknown" for missing parts.
    """
    parts = filename.replace(".txt", "").split("_")
    if len(parts) >= 5:
        return parts[0], parts[1], parts[2], parts[3], parts[4]
    title = filename.replace(".txt", "")
    return "Unknown", title, "Unknown", "Unknown", "Unknown"


def split_story(text: str, metadata: dict) -> List[dict]:
    """Chunk story text into 1000‑char windows with 200‑char overlap.
    Returns a list of LangChain Document dicts ready for *add_documents*.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([text], metadatas=[metadata])


# ---------------------------------------------------------------------------
# Main embedding routine
# ---------------------------------------------------------------------------

def embed_stories(folder: str = STORIES_DIR) -> None:
    """Walk *folder* recursively, embed every ``.txt`` story, and store it.

    @param folder: Path containing text stories.
    """
    api_key = get_openai_key()
    store   = init_vector_store(api_key)

    for root, _dirs, files in os.walk(folder):
        for fname in files:
            if not fname.endswith(".txt"):
                continue
            path = os.path.join(root, fname)
            author, title, year, genre, subgenre = parse_metadata(fname)
            with open(path, "r", encoding="utf-8") as fh:
                content = fh.read()
            docs = split_story(content, {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "subgenre": subgenre,
            })
            store.add_documents(docs)
            print(f"✅ Embedded '{title}' → {len(docs)} chunks")

    print("✅ Stories with genre and subgenre metadata have been embedded and stored in ChromaDB.")

# ---------------------------------------------------------------------------
# Script guard
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    embed_stories()

