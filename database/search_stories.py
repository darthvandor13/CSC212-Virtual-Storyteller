import os
import json
import openai
import chromadb
from langchain_openai import OpenAIEmbeddings

# Load API Keys
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("❌ OpenAI API key is missing. Set it as an environment variable.")

openai.api_key = openai_api_key

# Connect to ChromaDB using PersistentClient
CHROMA_DB_PATH = "/home/cvandor/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
vector_store = chroma_client.get_or_create_collection("stories")

# File to store user memory
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
    """Send a query to OpenAI's ChatGPT, using persistent memory."""
    messages = [{"role": "system", "content": "You are a skilled storyteller that remembers users' preferences."}]
    
    # Add past conversation history
    messages.extend(user_memory)

    # Add the new user query
    messages.append({"role": "user", "content": prompt})

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=500
    )

    # Store this exchange in memory
    user_memory.append({"role": "user", "content": prompt})
    user_memory.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content

def search_stories(query):
    """Search for stories similar to the user's request."""
    results = vector_store.query(
        query_texts=[query],
        n_results=3
    )

    if not results or not results['documents']:
        return []

    unique_results = []
    for i, doc in enumerate(results['documents'][0]):
        metadata = results['metadatas'][0][i]
        unique_results.append({
            "title": metadata.get("title", "Unknown Title"),
            "content": doc,
            "metadata": metadata
        })

    return unique_results

def summarize_story(story_content):
    """Generate a 1-2 sentence summary of a story."""
    return ask_chatgpt(f"Summarize this story in 1-2 sentences: {story_content[:500]}", [])

def refine_story_request(existing_query):
    """Allow users to refine their request if they want a different kind of story."""
    refinement = input("\n💡 Would you like to refine the story request? (yes/no): ").strip().lower()
    if refinement in ["yes", "y"]:
        new_request = input("✍ How would you like to change the story? (e.g., 'Make it about a space adventure' or 'I want a female protagonist'): ").strip()
        return new_request
    return existing_query

# Step 1: Ask for the user's name
username = input("\n👤 What's your name? ").strip().lower()
print(f"\n👋 Hello, {username.capitalize()}! I'll remember your preferences for future stories.")

# Load the user's past memory
user_memory = load_user_memory(username)

# Step 2: Ask if they want a story
user_input = input("\n📖 Would you like to hear a story? (yes/no): ").strip().lower()

if user_input not in ["yes", "y", "sure", "okay", "yes please", "absolutely", "of course", "why not", "tell me one"]:
    print("\n🎭 Maybe next time! Goodbye.")
    exit()

# Step 3: Ask what kind of story
story_request = input("\n🤔 What kind of story would you like to hear? (e.g., 'A brave knight' or 'A girl who learns to share'): ").strip()

# Step 4: Search for a similar story
matching_stories = search_stories(story_request)

if matching_stories:
    print("\n📚 I found some similar stories in my collection!")
    for i, story in enumerate(matching_stories):
        summary = summarize_story(story["content"])
        print(f"\n🔹 Story {i+1}: {story['title']}")
        print(f"📖 {summary}")

    user_choice = input("\nWould you like to hear one of these stories, or should I make up a new one? (existing/new): ").strip().lower()

    if user_choice == "existing":
        chosen_index = int(input("\nEnter the story number (1, 2, 3): ").strip()) - 1
        if 0 <= chosen_index < len(matching_stories):
            chosen_story = matching_stories[chosen_index]
            print(f"\n📖 Here is '{chosen_story['title']}':\n")
            print(chosen_story["content"])
        else:
            print("\n❌ Invalid choice. Generating a new story instead.")
            ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
            print(f"\n🤖 AI-Generated Story:\n📖 {ai_story}")
    else:
        print("\n📝 I’ll create a brand new story for you!")
        ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
        print(f"\n🤖 AI-Generated Story:\n📖 {ai_story}")

else:
    print("\n📖 I don’t have a story like that, but I can make one up for you!")
    ai_summary = ask_chatgpt(f"Summarize a story about {story_request} in 1-2 sentences.", user_memory)
    print(f"\n🎭 Here’s an idea: {ai_summary}")
    confirmation = input("Would you like me to tell this story? (yes/no): ").strip().lower()

    if confirmation == "yes":
        ai_story = ask_chatgpt(f"Tell me a full story about {story_request}", user_memory)
        print(f"\n🤖 AI-Generated Story:\n📖 {ai_story}")
    else:
        story_request = refine_story_request(story_request)
        ai_story = ask_chatgpt(f"Tell me a story about {story_request}", user_memory)
        print(f"\n🤖 AI-Generated Story:\n📖 {ai_story}")

# Save the updated memory
save_user_memory(username, user_memory)
