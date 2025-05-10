##! @file upload_stories.py
##! @brief  Bulk-upload EPUB/PDF stories into ChromaDB, with metadata & emojis.
##! @author Calvin Vandor

import os
import re
import chromadb
import pdfplumber
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up ChromaDB HttpClient
CHROMA_HOST = "34.118.162.201"  # Use the actual IP of your ChromaDB VM
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
vector_store = chroma_client.get_or_create_collection("stories")

# Load existing story titles to prevent duplicates
existing_docs = vector_store.get()
existing_titles = set(
    metadata.get("title", "").strip().lower()
    for metadata in existing_docs["metadatas"]
    if "title" in metadata
)

# Directory containing story subfolders
STORIES_DIR = "/home/cvandor/Projects/csc212/CSC212-Virtual-Storyteller/database/stories"

# Function to extract text from a PDF file
def extract_text_from_pdf(filepath):
    text = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text())
    return "\n".join(filter(None, text)).strip()

# Function to extract text from an EPUB file
def extract_text_from_epub(filepath):
    book = epub.read_epub(filepath)
    text = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, "html.parser")
            text.append(soup.get_text())
    return "\n".join(text).strip()

# Function to extract metadata from an EPUB file
def extract_metadata_from_epub(filepath):
    book = epub.read_epub(filepath)
    metadata = {
        "title": "Unknown",
        "author": "Unknown",
        "year": "Unknown",
        "genre": "Unknown",
        "subgenre": "Unknown"
    }
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

# Function to extract metadata from filename
def extract_metadata_from_filename(filename):
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

# Extract metadata with EPUB preference
def extract_metadata(filepath, file_type):
    if file_type == "EPUB3":
        metadata = extract_metadata_from_epub(filepath)
        if metadata["title"] != "Unknown":
            return metadata
    return extract_metadata_from_filename(filepath)

# Walk through directories and process stories
for root, _, files in os.walk(STORIES_DIR):
    file_groups = {}
    for filename in files:
        base_name = os.path.splitext(filename)[0]
        file_groups.setdefault(base_name, []).append(filename)

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

        metadata = extract_metadata(filepath, preferred_format)
        story_title = metadata["title"].strip().lower()

        if story_title in existing_titles:
            print(f"⏩ Skipping already-uploaded story: {metadata['title']}")
            continue

        if preferred_format == "EPUB3":
            story_content = extract_text_from_epub(filepath)
        else:
            story_content = extract_text_from_pdf(filepath)

        if not story_content.strip():
            print(f"⚠️ No readable text found in {filepath}, skipping.")
            continue

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        story_chunks = text_splitter.create_documents([story_content], metadatas=[metadata])

        # Split chunks for large story uploads
        chunk_ids = [f"{metadata['title']}_{i}" for i in range(len(story_chunks))]
        chunk_texts = [chunk.page_content for chunk in story_chunks]
        chunk_metadatas = [chunk.metadata for chunk in story_chunks]

        print(f"📌 Processing: {metadata['title']} ({preferred_format}) - Extracted {len(story_content.split())} words.")
        print(f"📦 Uploading {len(story_chunks)} chunks in batches...")

        BATCH_SIZE = 200  # safe upper limit for ChromaDB HTTPClient

        success = True
        for i in range(0, len(chunk_ids), BATCH_SIZE):
            batch_ids = chunk_ids[i:i + BATCH_SIZE]
            batch_docs = chunk_texts[i:i + BATCH_SIZE]
            batch_metas = chunk_metadatas[i:i + BATCH_SIZE]

            try:
                vector_store.add(
                    ids=batch_ids,
                    documents=batch_docs,
                    metadatas=batch_metas
                )
                print(f"   ✅ Uploaded batch {i // BATCH_SIZE + 1} of {((len(chunk_ids) - 1) // BATCH_SIZE) + 1}")
            except Exception as e:
                print(f"   ❌ Failed to upload batch {i // BATCH_SIZE + 1}: {e}")
                success = False
                break  # Stop on failure — you could also choose to continue

        if success:
            print(f"✅ Successfully added {metadata['title']} ({preferred_format}) to ChromaDB.\n")
        else:
            print(f"⚠️ Incomplete upload for {metadata['title']}. Review logs above.\n")

        existing_titles.add(story_title)  # Add to set to prevent future duplicates

print("\n✅ All stories have been processed and stored persistently in ChromaDB.")
