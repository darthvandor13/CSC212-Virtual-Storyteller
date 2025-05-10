##! @file search_stories.py
##! @brief  CLI tool: search ChromaDB for stories or create one with ChatGPT.
##! @author Calvin Vandor

import os
import json
import openai
import chromadb
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌OpenAI API key is missing. Set it in a .env file.")

openai.api_key = api_key

# Remote ChromaDB server URL
CHROMA_HOST = "34.118.162.201"          # Replace with your actual external VM IP

# Initialise ChromaDB client
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
vector_store  = chroma_client.get_or_create_collection("stories")

MEMORY_FILE = "user_memory.json"

def load_user_memory(username):
    """Load memory for a specific user from JSON storage."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory_data = json.load(file)
        return memory_data.get(username, [])
    return []

def save_user_memory(username, memory):
    """Save user-specific memory to a JSON file."""
    memory_data = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            memory_data = json.load(file)

    memory_data[username] = memory
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory_data, file, indent=4)

def ask_chatgpt(prompt, user_memory):
    """Send a query to OpenAI ChatGPT, using persistent memory."""
    messages = [
        {"role": "system",
         "content": "You are a skilled storyteller that remembers users' preferences."}
    ]
    messages.extend(user_memory)
    messages.append({"role": "user", "content": prompt})

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=300
    )

    # Store this exchange in memory
    user_memory.append({"role": "user",      "content": prompt})
    user_memory.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content

def search_stories(query):
    """Search for stories using ChromaDB's REST API."""
    results = vector_store.query(
        query_texts=[query],
        n_results=3
    )

    unique_results = []
    if results["documents"]:
        for i in range(len(results["documents"][0])):
            title   = results["metadatas"][0][i].get("title", "Unknown Title")
            snippet = results["documents"][0][i][:200]
            unique_results.append({
                "title":      title,
                "snippet":    snippet,
                "full_text":  results["documents"][0][i]
            })
    return unique_results

def refine_story_request(existing_query):
    """Ask the user if they want to refine their story request."""
    refine = input("\nWould you like to refine the story request? (yes/no): ").strip().lower()
    if refine in ["yes", "y"]:
        new_request = input(
            "How would you like to change the story "
            "(e.g., 'Make it about a space adventure'): "
        ).strip()
        return new_request
    return existing_query

# ----- Interactive flow -----------------------------------------------------

username = input("\nWhat is your name? ").strip().lower()
print(f"\nHello, {username.capitalize()}! I'll remember your preferences.")

user_memory = load_user_memory(username)

if input("\nWould you like to hear a story? (yes/no): ").strip().lower() \
        not in ["yes", "y", "sure", "okay", "yes please", "absolutely",
                "of course", "why not", "tell me one"]:
    print("\nMaybe next time! Goodbye.")
    exit()

story_request = input("\nWhat kind of story would you like to hear? ").strip()

matching_stories = search_stories(story_request)

if matching_stories:
    print("\nI found a similar story in my collection!")
    user_choice = input("Hear an existing story or create a new one? (existing/new): ").strip().lower()

    if user_choice == "existing":
        selected_story = matching_stories[0]
        title   = selected_story["title"]
        snippet = selected_story["snippet"]

        print(f"\nI have a story called '{title}'. Summary:\n{snippet}")
        if input("Would you like me to tell this story? (yes/no): ").strip().lower() == "yes":
            print(f"\nHere is '{title}':\n")
            print(selected_story["full_text"])
        else:
            story_request = refine_story_request(story_request)
            ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
            print(f"\nAI-Generated Story:\n{ai_story}")
    else:
        print("\nCreating a brand-new story for you!")
        ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
        print(f"\nAI-Generated Story:\n{ai_story}")

else:
    print("\nI don’t have a story like that, but I can make one up!")
    ai_summary = ask_chatgpt(f"Summarise a story about {story_request} in 1–2 sentences.", user_memory)
    print(f"\nHere’s an idea: {ai_summary}")
    if input("Would you like me to tell this story? (yes/no): ").strip().lower() == "yes":
        ai_story = ask_chatgpt(f"Tell me a full story about {story_request}", user_memory)
        print(f"\nAI-Generated Story:\n{ai_story}")
    else:
        story_request = refine_story_request(story_request)
        ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
        print(f"\nAI-Generated Story:\n{ai_story}")

save_user_memory(username, user_memory)

