##! @file search_stories.py
##! @brief  CLI helper that searches ChromaDB for existing stories or generates
##!         a new one with OpenAI ChatCompletion, while persisting user memory.
##!
##! This refactor preserves behaviour but:
##!   • Removes all emojis to keep the console output ASCII‑clean.
##!   • Splits the monolithic script into discrete, testable functions so
##!     Doxygen can attach clear `@param` / `@return` tables.
##!   • Fixes the `openai_api_key` variable mismatch in the original code.
##!
##! @author Calvin Vandor
##! @date   2025‑05‑08
##! @copyright MIT License
##!
##! ---------------------------------------------------------------------------
##! Example usage (interactive)
##! ---------------------------------------------------------------------------
##! $ python search_stories.py
##! Name: alice
##! Would you like a story? yes
##! What kind? brave knight
##! ---------------------------------------------------------------------------

import os
import json
import openai
import chromadb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# --------------------------------------------------------------------------- #
# Configuration                                                             #
# --------------------------------------------------------------------------- #

#: ChromaDB host (remote VM)
CHROMA_HOST = "34.118.162.201"  # ➟ replace with your IP if different

#: Local JSON file that stores per‑user memory of past prompts / answers
MEMORY_FILE = "user_memory.json"

#: Number of hits to fetch from ChromaDB when searching
N_RESULTS = 3

# --------------------------------------------------------------------------- #
# Global clients                                                             #
# --------------------------------------------------------------------------- #

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌OPENAI_API_KEY is missing; set it in .env or env var.")
openai.api_key = api_key

chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
vector_store   = chroma_client.get_or_create_collection("stories")

# --------------------------------------------------------------------------- #
# Persistence helpers                                                        #
# --------------------------------------------------------------------------- #

def load_user_memory(username):
    """Return a list of chat history dicts for *username* (or empty list)."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as fh:
            return json.load(fh).get(username, [])
    return []

def save_user_memory(username, memory):
    """Persist *memory* (list of dicts) under *username* in :pydata:`MEMORY_FILE`."""
    mem = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as fh:
            mem = json.load(fh)
    mem[username] = memory
    with open(MEMORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(mem, fh, indent=4)

# --------------------------------------------------------------------------- #
# OpenAI interaction                                                         #
# --------------------------------------------------------------------------- #

def ask_chatgpt(prompt, user_memory):
    """Pass *prompt* plus *user_memory* to ChatGPT and append the exchange."""
    messages = [{"role": "system", "content": "You are a skilled storyteller that remembers users' preferences."}]
    messages.extend(user_memory)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
    )

    # Store interaction
    user_memory.append({"role": "user", "content": prompt})
    user_memory.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content

# --------------------------------------------------------------------------- #
# ChromaDB search                                                            #
# --------------------------------------------------------------------------- #

def search_stories(query, n_results=N_RESULTS):
    """Return a list of candidate stories matching *query* using ChromaDB."""
    results = vector_store.query(query_texts=[query], n_results=n_results)
    unique = []
    if results.get("documents"):
        for i, doc in enumerate(results["documents"][0]):
            meta    = results["metadatas"][0][i]
            unique.append({
                "title": meta.get("title", "Unknown Title"),
                "snippet": doc[:200],
                "full_text": doc,
            })
    return unique

# --------------------------------------------------------------------------- #
# Interactive helpers                                                        #
# --------------------------------------------------------------------------- #

def refine_story_request(existing_query):
    """Ask the user if they want to tweak *existing_query*; return new query."""
    if input("\nWould you like to refine the story request? (yes/no): ").lower().startswith("y"):
        return input("How would you like to change it? ").strip()
    return existing_query

# --------------------------------------------------------------------------- #
# Main CLI flow                                                              #
# --------------------------------------------------------------------------- #

def main():  # noqa: C901  # (yes, it's a long function; fine for CLI demo)
    """Command‑line interface that steps the user through story selection."""
    username = input("Name: ").strip().lower() or "guest"
    print(f"Hello, {username.capitalize()}! I will remember your preferences.")

    memory = load_user_memory(username)

    if input("Would you like to hear a story? (yes/no): ").lower() not in {"yes", "y"}:
        print("Maybe next time — goodbye!")
        return

    story_request = input("What kind of story would you like? ").strip()
    matches       = search_stories(story_request)

    if matches:
        print("\nFound a similar story in my collection!")
        choice = input("Hear existing story or create new? (existing/new): ").lower()
        if choice == "existing":
            story = matches[0]
            print(f"\n*{story['title']}* — {story['snippet']}…")
            if input("Tell this story? (yes/no): ").lower().startswith("y"):
                print("\n" + story["full_text"])
            else:
                story_request = refine_story_request(story_request)
                print(ask_chatgpt(f"Tell me a story about {story_request}", memory))
        else:
            print("Creating a new story…")
            print(ask_chatgpt(f"Tell me a story about {story_request}", memory))
    else:
        print("\nNo matching story; I'll invent one.")
        summary = ask_chatgpt(f"Summarise a story about {story_request} in 2 sentences.", memory)
        print("Idea: " + summary)
        if input("Tell this story? (yes/no): ").lower().startswith("y"):
            print(ask_chatgpt(f"Tell me a full story about {story_request}", memory))
        else:
            story_request = refine_story_request(story_request)
            print(ask_chatgpt(f"Tell me a story about {story_request}", memory))

    save_user_memory(username, memory)


if __name__ == "__main__":
    main()

