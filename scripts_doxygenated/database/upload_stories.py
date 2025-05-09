##! @file upload_stories.py
##! @brief  Bulk uploader that scans local story folders, extracts text &
##!         metadata (EPUB3 or PDF), splits into chunks and inserts them into a
##!         remote ChromaDB collection.
##!
##! This refactor retains the original emoji‑rich console output but breaks the
##! monster script into helper functions so Doxygen can provide clean parameter
##! tables, return values, and call graphs.  Runtime logic is unchanged.
##!
##! @author Calvin Vandor
##! @date   2025-05-08
##! @copyright MIT License
##!

from __future__ import annotations

import os
import re
import chromadb
import pdfplumber
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CHROMA_HOST: str = "34.118.162.201"  # ❗ replace with your own external VM IP
STORIES_DIR: str = os.path.join(os.path.dirname(__file__), "stories")
COLLECTION   = "stories"
MEMORY_BATCH = 200  #: safe upper‑limit for Chroma HTTPClient per request

# ---------------------------------------------------------------------------
# Initialise Chroma client
# ---------------------------------------------------------------------------

print(f"🔗 Connecting to ChromaDB at {CHROMA_HOST} …")
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=8000)
vector_store  = chroma_client.get_or_create_collection(COLLECTION)

existing_titles = {
    md.get("title", "").strip().lower()
    for md in vector_store.get()["metadatas"]
    if "title" in md
}

# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def extract_text_from_pdf(filepath: str) -> str:
    """Return raw text extracted from every page of a PDF."""
    pages: List[str] = []
    with pdfplumber.open(filepath) as pdf:
        pages.extend(page.extract_text() or "" for page in pdf.pages)
    return "\n".join(filter(None, pages)).strip()


def extract_text_from_epub(filepath: str) -> str:
    """Return concatenated plaintext from every XHTML item in an EPUB."""
    book = epub.read_epub(filepath)
    texts: List[str] = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.content, "html.parser")
            texts.append(soup.get_text())
    return "\n".join(texts).strip()


def extract_metadata_from_epub(filepath: str) -> Dict[str, str]:
    """Prefer embedded EPUB metadata when available."""
    book = epub.read_epub(filepath)
    md = {k: "Unknown" for k in ("title", "author", "year", "genre", "subgenre")}
    if (t := book.get_metadata("DC", "title")):
        md["title"] = t[0][0]
    if (c := book.get_metadata("DC", "creator")):
        md["author"] = c[0][0]
    if (d := book.get_metadata("DC", "date")):
        md["year"] = d[0][0]
    if (s := book.get_metadata("DC", "subject")):
        md["genre"]    = s[0][0]
        md["subgenre"] = s[1][0] if len(s) > 1 else "Unknown"
    return md


def extract_metadata_from_filename(filename: str) -> Dict[str, str]:
    """Fallback parser: author_title_year_genre_subgenre.[txt|pdf|epub]"""
    name = os.path.basename(filename)
    parts = re.split(r"[_\-]", name.rsplit(".", 1)[0])
    if len(parts) >= 5:
        return dict(zip(("author", "title", "year", "genre", "subgenre"), parts[:5]))
    return {
        "author": "Unknown",
        "title":  parts[1] if len(parts) > 1 else name,
        "year":   "Unknown",
        "genre":  "Unknown",
        "subgenre": "Unknown",
    }


def choose_preferred_format(file_list: List[str]) -> Tuple[str, str] | Tuple[None, None]:
    """Return (filepath, format) choosing EPUB over PDF when available."""
    base = os.path.dirname(file_list[0])
    stem = os.path.splitext(file_list[0])[0]
    if any(f.endswith(".epub") for f in file_list):
        return os.path.join(base, f"{stem}.epub"), "EPUB3"
    if any(f.endswith(".pdf") for f in file_list):
        return os.path.join(base, f"{stem}.pdf"), "PDF"
    return None, None


def split_story(text: str, metadata: Dict[str, str]):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.create_documents([text], metadatas=[metadata])


def upload_chunks(ids, docs, metas):
    total = len(ids)
    for i in range(0, total, MEMORY_BATCH):
        batch_ids   = ids[i:i + MEMORY_BATCH]
        batch_docs  = docs[i:i + MEMORY_BATCH]
        batch_metas = metas[i:i + MEMORY_BATCH]
        vector_store.add(ids=batch_ids, documents=batch_docs, metadatas=batch_metas)
        print(f"   ✅ Uploaded batch {i // MEMORY_BATCH + 1} / {((total - 1) // MEMORY_BATCH) + 1}")


# ---------------------------------------------------------------------------
# Main ingestion loop
# ---------------------------------------------------------------------------

for root, _, files in os.walk(STORIES_DIR):
    grouped = {}
    for f in files:
        grouped.setdefault(os.path.splitext(f)[0], []).append(f)

    for stem, flist in grouped.items():
        fp, fmt = choose_preferred_format(flist)
        if not fp:
            print(f"⚠️  No EPUB or PDF found for {stem}, skipping.")
            continue

        metadata = extract_metadata_from_epub(fp) if fmt == "EPUB3" else extract_metadata_from_filename(fp)
        title_key = metadata["title"].strip().lower()
        if title_key in existing_titles:
            print(f"⏩ Skipping already-uploaded story: {metadata['title']}")
            continue

        story_text = extract_text_from_epub(fp) if fmt == "EPUB3" else extract_text_from_pdf(fp)
        if not story_text.strip():
            print(f"⚠️  No readable text in {fp}, skipping.")
            continue

        chunks = split_story(story_text, metadata)
        ids    = [f"{metadata['title']}_{i}" for i in range(len(chunks))]
        docs   = [c.page_content for c in chunks]
        metas  = [c.metadata for c in chunks]

        print(f"📌 Processing: {metadata['title']} ({fmt}) — {len(story_text.split())} words.")
        print(f"📦 Uploading {len(chunks)} chunks …")

        try:
            upload_chunks(ids, docs, metas)
            existing_titles.add(title_key)
            print(f"✅ Successfully added {metadata['title']} ({fmt}) to ChromaDB.\n")
        except Exception as exc:
            print(f"❌ Failed to upload {metadata['title']}: {exc}\n")

print("\n✅ All stories processed and stored in ChromaDB.")

