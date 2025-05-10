##! @file upload_stories.py
##! @brief Bulk-uploads EPUB/PDF stories into ChromaDB with metadata.
##! @details
##! This script scans a specified directory for story subfolders containing EPUB or PDF files.
##! It extracts text content and metadata (preferring EPUB internal metadata, then
##! falling back to filename-derived metadata if EPUB title is poor).
##! The extracted text is split into chunks and uploaded to a ChromaDB collection in batches.
##! The script avoids uploading duplicate stories based on titles already present in the database.
##! Configuration for ChromaDB connection, story directory, and batch size can be
##! set via environment variables.
##!
##! @author Calvin Vandor
##! @date 2025-05-10
##! @version 1.2
##! @copyright MIT License

from __future__ import annotations # For postponed evaluation of type hints

import os
import re
import chromadb
import pdfplumber
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Dict, List, Tuple, Optional, Set

# --- Configuration (from Environment Variables with Defaults) ---

## @var CHROMA_HOST
# Hostname or IP address of the ChromaDB server.
CHROMA_HOST: str = os.getenv("CHROMA_HOST", "localhost")

## @var CHROMA_PORT
# Port number for the ChromaDB server.
CHROMA_PORT: int = int(os.getenv("CHROMA_PORT", "8000"))

## @var COLLECTION_NAME
# Name of the ChromaDB collection to use for stories.
COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "stories")

## @var DEFAULT_STORIES_DIR
# Default relative path for the stories directory.
DEFAULT_STORIES_DIR: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stories")

## @var STORIES_DIR
# Directory containing story files/subfolders. Expected to be relative to this script
# (in a 'stories' subdirectory) by default, but can be overridden by an environment variable.
STORIES_DIR: str = os.getenv("STORIES_DIR", DEFAULT_STORIES_DIR)

## @var BATCH_SIZE
# Number of document chunks to upload to ChromaDB in a single batch.
BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))

# --- ChromaDB Client Initialization ---
print(f"🔗 Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT} ...")
try:
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    vector_store = chroma_client.get_or_create_collection(COLLECTION_NAME)
    print(f"✅ Successfully connected and using collection '{COLLECTION_NAME}'.")
except Exception as e:
    print(f"❌ CRITICAL: Could not connect to ChromaDB or get/create collection: {e}")
    print("   Please ensure ChromaDB is running and accessible, and configuration is correct.")
    exit(1) # Exit if DB connection fails at startup

# --- Load Existing Story Titles to Prevent Duplicates ---
print("ℹ️ Loading existing story titles from ChromaDB to prevent duplicates...")
try:
    existing_docs_data = vector_store.get() # Fetch all docs to get metadatas
    existing_titles: Set[str] = {
        metadata.get("title", "").strip().lower()
        for metadata in existing_docs_data.get("metadatas", [])
        if metadata and metadata.get("title") # Ensure metadata and title exist
    }
    print(f"Loaded {len(existing_titles)} existing titles.")
except Exception as e:
    print(f"⚠️ Warning: Could not fetch existing titles from ChromaDB: {e}. Duplicate checking might be affected.")
    existing_titles: Set[str] = set()


# --- Utility Functions ---

def extract_text_from_pdf(filepath: str) -> str:
    """
    Extracts raw text content from all pages of a PDF file.

    @param filepath The path to the PDF file.
    @return A string containing the concatenated text from the PDF, or an empty string if extraction fails.
    """
    print(f"📄 Extracting text from PDF: {os.path.basename(filepath)}")
    text_pages: List[str] = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text: # Only append if text was actually extracted
                    text_pages.append(page_text)
        return "\n".join(text_pages).strip()
    except Exception as e:
        print(f"❌ Error extracting text from PDF '{filepath}': {e}")
        return ""

def extract_text_from_epub(filepath: str) -> str:
    """
    Extracts concatenated plaintext content from all XHTML items in an EPUB file.

    @param filepath The path to the EPUB file.
    @return A string containing the concatenated text from the EPUB, or an empty string if extraction fails.
    """
    print(f"📚 Extracting text from EPUB: {os.path.basename(filepath)}")
    texts: List[str] = []
    try:
        book = epub.read_epub(filepath)
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.content, "html.parser")
                texts.append(soup.get_text())
        return "\n".join(texts).strip()
    except Exception as e:
        print(f"❌ Error extracting text from EPUB '{filepath}': {e}")
        return ""

def extract_metadata_from_epub(filepath: str) -> Dict[str, str]:
    """
    Extracts metadata (title, author, year, genre, subgenre) from an EPUB file.
    Defaults to "Unknown" if a field is not found.

    @param filepath The path to the EPUB file.
    @return A dictionary containing the extracted metadata.
    """
    print(f"📚 Extracting metadata from EPUB: {os.path.basename(filepath)}")
    metadata = {k: "Unknown" for k in ("title", "author", "year", "genre", "subgenre")}
    try:
        book = epub.read_epub(filepath)
        if title_meta := book.get_metadata("DC", "title"):
            metadata["title"] = title_meta[0][0].strip()
        if creator_meta := book.get_metadata("DC", "creator"):
            metadata["author"] = creator_meta[0][0].strip()
        if date_meta := book.get_metadata("DC", "date"):
            # EPUB date can be YYYY-MM-DD or just YYYY. Extract year part.
            year_match = re.search(r'\d{4}', date_meta[0][0])
            if year_match:
                metadata["year"] = year_match.group(0)
        if subject_meta := book.get_metadata("DC", "subject"):
            subjects = [s[0].strip() for s in subject_meta if s and s[0].strip()]
            if subjects:
                metadata["genre"] = subjects[0]
            if len(subjects) > 1:
                metadata["subgenre"] = subjects[1]
    except Exception as e:
        print(f"⚠️ Warning: Could not extract full metadata from EPUB '{filepath}': {e}. Some fields might be 'Unknown'.")
    return metadata

def extract_metadata_from_filename(filepath: str) -> Dict[str, str]:
    """
    Extracts metadata from a filename assuming a pattern like:
    Author_Title_Year_Genre_Subgenre.extension
    Uses underscores or hyphens as delimiters. Defaults to "Unknown" or the filename stem.

    @param filepath The path to the file.
    @return A dictionary containing the extracted metadata.
    """
    filename_stem = os.path.splitext(os.path.basename(filepath))[0]
    parts = [p.strip() for p in re.split(r'[_\-]', filename_stem) if p.strip()] # Split and remove empty strings

    if len(parts) >= 5:
        return {
            "author": parts[0],
            "title": parts[1],
            "year": parts[2],
            "genre": parts[3],
            "subgenre": parts[4]
        }
    else: # Fallback if filename doesn't match the full pattern
        title = parts[1] if len(parts) > 1 else (parts[0] if len(parts) == 1 else filename_stem)
        return {
            "author": parts[0] if len(parts) > 0 and len(parts) != 1 else "Unknown", # Avoid assigning title as author if only one part
            "title": title,
            "year": "Unknown",
            "genre": "Unknown",
            "subgenre": "Unknown"
        }

def get_story_metadata(filepath: str, file_format: Optional[str]) -> Dict[str, str]:
    """
    Extracts metadata for a story, preferring EPUB internal metadata.
    If EPUB metadata provides an "Unknown" or empty title, it attempts to use
    metadata derived from the filename as a fallback for the entire metadata dictionary.
    For non-EPUB files, it directly uses filename-derived metadata.

    @param filepath The full path to the story file.
    @param file_format The format of the file (e.g., "EPUB3", "PDF").
    @return A dictionary containing the story's metadata.
    """
    if file_format == "EPUB3":
        epub_metadata = extract_metadata_from_epub(filepath)
        epub_title = epub_metadata.get("title", "Unknown").strip()

        if not epub_title or epub_title.lower() == "unknown":
            print(f"ℹ️ EPUB title for '{os.path.basename(filepath)}' is unsatisfactory ('{epub_title}'). Using filename metadata as fallback.")
            filename_metadata = extract_metadata_from_filename(filepath)
            # Prioritize filename metadata if its title is more definitive
            filename_title = filename_metadata.get("title", "Unknown").strip()
            if filename_title and filename_title.lower() != "unknown":
                return filename_metadata
        return epub_metadata # Return EPUB metadata if title is good, or if filename fallback also wasn't better
    else: # For PDF or other types
        return extract_metadata_from_filename(filepath)


def choose_preferred_format(root_dir: str, file_group: List[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Chooses a preferred file format (EPUB over PDF) from a list of files with the same base name.

    @param root_dir The root directory where these files are located.
    @param file_group A list of filenames (e.g., ['story.epub', 'story.pdf', 'story.txt']).
    @return A tuple containing (filepath_to_process, format_string) or (None, None) if no preferred format is found.
    """
    if not file_group:
        return None, None

    base_name_with_ext = file_group[0] # e.g., "MyStory.epub"
    base_name = os.path.splitext(base_name_with_ext)[0] # e.g., "MyStory"

    # Check for EPUB first
    if any(f.lower().endswith(".epub") for f in file_group):
        return os.path.join(root_dir, f"{base_name}.epub"), "EPUB3"
    # Then check for PDF
    if any(f.lower().endswith(".pdf") for f in file_group):
        return os.path.join(root_dir, f"{base_name}.pdf"), "PDF"
    return None, None


def split_story_into_chunks(story_text: str, metadata: Dict[str, str], chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits a long story text into smaller chunks using RecursiveCharacterTextSplitter.

    @param story_text The full text of the story.
    @param metadata The metadata dictionary to associate with each chunk.
    @param chunk_size The maximum size of each chunk.
    @param chunk_overlap The overlap between consecutive chunks.
    @return A list of Langchain Document objects (chunks).
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    # Langchain's create_documents expects a list of texts and a list of metadatas (or one metadata for all)
    return text_splitter.create_documents([story_text], metadatas=[metadata])


def upload_story_chunks_to_chromadb(story_title: str, story_chunks_docs: List, batch_size: int = BATCH_SIZE):
    """
    Uploads story chunks (Langchain Document objects) to ChromaDB in batches.

    @param story_title The title of the story, used for generating chunk IDs.
    @param story_chunks_docs A list of Langchain Document objects.
    @param batch_size The number of chunks to upload per batch.
    @return True if all batches were uploaded successfully, False otherwise.
    """
    chunk_ids = [f"{story_title}_{i}" for i in range(len(story_chunks_docs))]
    chunk_texts = [chunk.page_content for chunk in story_chunks_docs]
    chunk_metadatas = [chunk.metadata for chunk in story_chunks_docs]

    total_chunks = len(chunk_ids)
    num_batches = ((total_chunks - 1) // batch_size) + 1 if total_chunks > 0 else 0

    print(f"📦 Uploading {total_chunks} chunks for '{story_title}' in {num_batches} batches (size: {batch_size})...")

    for i in range(0, total_chunks, batch_size):
        batch_num = (i // batch_size) + 1
        batch_ids = chunk_ids[i:i + batch_size]
        batch_docs = chunk_texts[i:i + batch_size]
        batch_metas = chunk_metadatas[i:i + batch_size]

        try:
            vector_store.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metas
            )
            print(f"    ✅ Uploaded batch {batch_num} of {num_batches}")
        except Exception as e:
            print(f"    ❌ Failed to upload batch {batch_num} for '{story_title}': {e}")
            return False # Stop on failure for this story
    return True

# --- Main Ingestion Loop ---
def main_ingestion_loop():
    """
    Walks through the STORIES_DIR, processes each story (EPUB or PDF),
    extracts content and metadata, and uploads it to ChromaDB.
    """
    print(f"\n🚀 Starting story ingestion from directory: {STORIES_DIR}")
    if not os.path.isdir(STORIES_DIR):
        print(f"❌ Error: Stories directory not found: {STORIES_DIR}")
        return

    processed_files_count = 0
    successfully_uploaded_stories = 0

    for root, _, files in os.walk(STORIES_DIR):
        if not files:
            continue

        # Group files by their base name (e.g., "MyStory" for "MyStory.epub", "MyStory.pdf")
        file_groups: Dict[str, List[str]] = {}
        for filename in files:
            if filename.lower().endswith((".epub", ".pdf")): # Process only EPUB and PDF
                base_name = os.path.splitext(filename)[0]
                file_groups.setdefault(base_name, []).append(filename)

        for base_name, file_list in file_groups.items():
            processed_files_count +=1
            print(f"\n--- Processing group: {base_name} ---")
            filepath_to_process, file_format = choose_preferred_format(root, file_list)

            if not filepath_to_process or not file_format:
                print(f"⚠️ No processable EPUB or PDF found for base name '{base_name}' in '{root}', skipping.")
                continue

            print(f"✨ Selected file: {os.path.basename(filepath_to_process)} (Format: {file_format})")
            metadata = get_story_metadata(filepath_to_process, file_format)
            story_title_key = metadata.get("title", "").strip().lower()

            if not story_title_key or story_title_key == "unknown":
                print(f"⚠️ Skipping '{os.path.basename(filepath_to_process)}' due to missing or 'Unknown' title in metadata.")
                continue

            if story_title_key in existing_titles:
                print(f"⏩ Skipping already-uploaded story (title: '{metadata['title']}')")
                continue

            if file_format == "EPUB3":
                story_content = extract_text_from_epub(filepath_to_process)
            elif file_format == "PDF":
                story_content = extract_text_from_pdf(filepath_to_process)
            else: # Should not happen due to choose_preferred_format logic
                print(f"❓ Unknown format '{file_format}' for {filepath_to_process}, skipping.")
                continue

            if not story_content.strip():
                print(f"⚠️ No readable text content found in '{os.path.basename(filepath_to_process)}', skipping.")
                continue

            print(f"📝 Extracted ~{len(story_content.split())} words from '{metadata['title']}'. Splitting into chunks...")
            story_chunks = split_story_into_chunks(story_content, metadata)

            if not story_chunks:
                print(f"⚠️ Could not split '{metadata['title']}' into chunks, skipping.")
                continue

            upload_successful = upload_story_chunks_to_chromadb(metadata["title"], story_chunks)

            if upload_successful:
                print(f"✅ Successfully processed and added '{metadata['title']}' to ChromaDB.")
                existing_titles.add(story_title_key) # Add to set to prevent re-processing in this run
                successfully_uploaded_stories +=1
            else:
                print(f"⚠️ Incomplete upload for '{metadata['title']}'. Review logs above.")
    
    print(f"\n--- Ingestion Summary ---")
    print(f"Processed {processed_files_count} file groups.")
    print(f"Successfully uploaded {successfully_uploaded_stories} new stories to ChromaDB.")
    print("✅ Story ingestion process complete.")

if __name__ == "__main__":
    main_ingestion_loop()
