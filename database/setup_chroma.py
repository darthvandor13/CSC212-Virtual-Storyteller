##! @file setup_chroma.py
##! @brief  Embed story text files into ChromaDB with genre metadata.
##! @author Calvin Vandor

import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("❌ OpenAI API key is missing. Set it as an environment variable.")

# Initialise ChromaDB client
vector_store = Chroma(
    collection_name="stories",
    embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key),
    persist_directory="./chroma_db"
)

# Directory where stories are stored
stories_dir = os.path.join(os.path.dirname(__file__), "stories")

for filename in os.listdir(stories_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(stories_dir, filename)

        # Extract metadata (assumes format author_title_year_genre_subgenre.txt)
        parts = filename.replace(".txt", "").split("_")
        if len(parts) >= 5:
            author, title, year, genre, subgenre = parts[:5]
        else:
            author, title, year, genre, subgenre = (
                "Unknown", filename.replace(".txt", ""), "Unknown", "Unknown", "Unknown"
            )

        with open(filepath, "r", encoding="utf-8") as file:
            story_content = file.read()

        # Split story into chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        story_chunks = splitter.create_documents(
            [story_content],
            metadatas=[{
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "subgenre": subgenre
            }]
        )

        # Store in ChromaDB
        vector_store.add_documents(story_chunks)

print("✅ Stories with genre and subgenre metadata have been embedded and stored in ChromaDB.")

