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

# Define the remote ChromaDB server URL
CHROMA_HOST = "34.118.162.201"  # Replace with your actual external VM IP

# Initialize the ChromaDB client with remote server settings
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
vector_store = chroma_client.get_or_create_collection("stories")

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
        max_tokens=300
    )

    # Store this exchange in memory
    user_memory.append({"role": "user", "content": prompt})
    user_memory.append({"role": "assistant", "content": response.choices[0].message.content})

    return response.choices[0].message.content

def search_stories(query):
    """Search for stories using ChromaDB's REST API."""
    results = vector_store.query(
        query_texts=[query],  # ChromaDB expects a list of queries
        n_results=3  # Number of results to return
    )

    # Ensure results are properly formatted
    unique_results = []
    if results["documents"]:  # Ensure there are results before accessing
        for i in range(len(results["documents"][0])):
            title = results["metadatas"][0][i].get("title", "Unknown Title")
            snippet = results["documents"][0][i][:200]  # Get the first 200 characters
            unique_results.append({"title": title, "snippet": snippet, "full_text": results["documents"][0][i]})

    return unique_results

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
    print("\n📚 I found a similar story in my collection!")
    user_choice = input("Would you like to hear an existing story, or should I make up a new one? (existing/new): ").strip().lower()

    if user_choice == "existing":
        selected_story = matching_stories[0]  # ChromaDB returns a dictionary, not an object

        title = selected_story["title"]
        snippet = selected_story["snippet"]

        print(f"\n🎭 I have a story called '{title}'. Here’s a brief summary:\n📜 {snippet}")
        confirmation = input("Would you like me to tell this story? (yes/no): ").strip().lower()

        if confirmation == "yes":
            print(f"\n📖 Here is '{title}':\n")
            print(selected_story["full_text"])
        else:
            story_request = refine_story_request(story_request)
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

