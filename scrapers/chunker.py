"""
Production Chunker for IDEAM RAG
--------------------------------
• Merges content properly
• Creates ~450-word chunks
• Removes duplicate chunks
• Saves processed CSV
"""

import json
import os
import pandas as pd

# ===== PATH CONFIG =====
CURRENT_FILE = os.path.abspath(__file__)
SCRAPERS_DIR = os.path.dirname(CURRENT_FILE)
PROJECT_ROOT = os.path.dirname(SCRAPERS_DIR)

RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "ideam_raw.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data", "processed", "ideam_chunks.csv")

CHUNK_SIZE = 450


def load_raw_data():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_text_blocks(page):
    chunks = []
    buffer = []

    for block in page["content"]:
        heading = block.get("heading", "")
        text = block.get("text", "")

        combined = f"{heading}. {text}" if heading else text
        words = combined.split()

        buffer.extend(words)

        while len(buffer) >= CHUNK_SIZE:
            chunk = " ".join(buffer[:CHUNK_SIZE])
            chunks.append(chunk)
            buffer = buffer[CHUNK_SIZE:]

    if buffer:
        chunks.append(" ".join(buffer))

    return chunks


def process_and_save():
    raw_data = load_raw_data()
    all_chunks = []
    seen_chunks = set()

    for page in raw_data:
        page_url = page["url"]
        title = page.get("title", "")

        page_chunks = chunk_text_blocks(page)

        for chunk in page_chunks:
            if len(chunk.split()) > 100:
                if chunk not in seen_chunks:
                    all_chunks.append({
                        "page_url": page_url,
                        "title": title,
                        "content": chunk
                    })
                    seen_chunks.add(chunk)

    df = pd.DataFrame(all_chunks)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("Chunks saved to:", OUTPUT_FILE)
    print("Total chunks:", len(df))
    print("Average words:", df["content"].apply(lambda x: len(x.split())).mean())


if __name__ == "__main__":
    process_and_save()