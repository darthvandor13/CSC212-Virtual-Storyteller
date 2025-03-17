import os
import re
import chromadb
import pdfplumber
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up ChromaDB PersistentClient
CHROMA_DB_PATH = "/home/cvandor/chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
vector_store = chroma_client.get_or_create_collection("stories")

# Directory containing story subfolders
STORIES_DIR = "/home/cvandor/Projects/csc212/database/stories"

# Function to extract text from a PDF file
def extract_text_from_pdf(filepath):
    """Extract text from a PDF file using pdfplumber."""
    text = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text())
    return "\n".join(filter(None, text)).strip()  # Remove empty lines

# Function to extract text from an EPUB file
def extract_text_from_epub(filepath):
    """Extract text from an EPUB file using ebooklib & BeautifulSoup."""
    book = epub.read_epub(filepath)
    text = []
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, "html.parser")
            text.append(soup.get_text())

    return "\n".join(text).strip()

# Function to extract metadata from an EPUB file
def extract_metadata_from_epub(filepath):
    """Extracts metadata (title, author, genre, etc.) from an EPUB file."""
    book = epub.read_epub(filepath)
    metadata = {
        "title": "Unknown",
        "author": "Unknown",
        "year": "Unknown",
        "genre": "Unknown",
        "subgenre": "Unknown"
    }

    # Extract metadata from EPUB
    if book.get_metadata("DC", "title"):
        metadata["title"] = book.get_metadata("DC", "title")[0][0]
    if book.get_metadata("DC", "creator"):
        metadata["author"] = book.get_metadata("DC", "creator")[0][0]
    if book.get_metadata("DC", "date"):
        metadata["year"] = book.get_metadata("DC", "date")[0][0]
    if book.get_metadata("DC", "subject"):
        subjects = book.get_metadata("DC", "subject")
        metadata["genre"] = subjects[0][0] if subjects else "Unknown"
        metadata["subgenre"] = subjects[1][0] if len(subjects) > 1 else "Unknown"

    return metadata

# Function to extract metadata from filename (fallback if EPUB metadata missing)
def extract_metadata_from_filename(filename):
    """Attempts to extract title, author, genre, etc., from filenames."""
    filename = os.path.basename(filename)
    name_parts = re.split(r'[_\-]', filename.replace(".txt", "").replace(".pdf", "").replace(".epub", ""))
    
    if len(name_parts) >= 5:
        return {
            "author": name_parts[0],
            "title": name_parts[1],
            "year": name_parts[2],
            "genre": name_parts[3],
            "subgenre": name_parts[4]
        }
    return {
        "author": "Unknown",
        "title": filename.replace(".txt", "").replace(".pdf", "").replace(".epub", ""),
        "year": "Unknown",
        "genre": "Unknown",
        "subgenre": "Unknown"
    }

# Function to extract metadata (prefers EPUB metadata, falls back to filename)
def extract_metadata(filepath, file_type):
    """Extract metadata from EPUB if available, otherwise fallback to filename."""
    if file_type == "EPUB3":
        epub_metadata = extract_metadata_from_epub(filepath)
        if epub_metadata["title"] != "Unknown":  # Valid metadata found
            return epub_metadata

    # Fallback: Extract from filename
    return extract_metadata_from_filename(filepath)

# Walk through all subdirectories and process files
for root, _, files in os.walk(STORIES_DIR):
    # Identify files by base story name (without extension)
    file_groups = {}

    for filename in files:
        base_name = os.path.splitext(filename)[0]  # Remove file extension
        file_groups.setdefault(base_name, []).append(filename)

    # Process files, prioritizing EPUB3 > PDF > Ignore TXT
    for base_name, file_list in file_groups.items():
        filepath = None
        preferred_format = None

        if any(f.endswith(".epub") for f in file_list):
            filepath = os.path.join(root, f"{base_name}.epub")
            preferred_format = "EPUB3"
        elif any(f.endswith(".pdf") for f in file_list):
            filepath = os.path.join(root, f"{base_name}.pdf")
            preferred_format = "PDF"
        else:
            print(f"⚠️ No EPUB or PDF found for {base_name}, skipping.")
            continue

        # Extract text based on chosen format
        if preferred_format == "EPUB3":
            story_content = extract_text_from_epub(filepath)
        else:
            story_content = extract_text_from_pdf(filepath)

        if not story_content.strip():
            print(f"⚠️ No readable text found in {filepath}, skipping.")
            continue

        # Extract metadata
        metadata = extract_metadata(filepath, preferred_format)

        # Split long stories into chunks for better vector search
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        story_chunks = text_splitter.create_documents([story_content], metadatas=[metadata])

        # ✅ Optimized: Batch all chunks before inserting into ChromaDB
        chunk_ids = [f"{metadata['title']}_{i}" for i in range(len(story_chunks))]
        chunk_texts = [chunk.page_content for chunk in story_chunks]
        chunk_metadatas = [chunk.metadata for chunk in story_chunks]

        vector_store.add(
            ids=chunk_ids,
            documents=chunk_texts,
            metadatas=chunk_metadatas
        )

        print(f"✅ Successfully added {metadata['title']} ({preferred_format}) to ChromaDB.")

print("\n✅ All stories have been processed and stored persistently in ChromaDB.")

