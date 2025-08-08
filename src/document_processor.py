# src/document_processor.py

import os
import re

BASE_DIR = r"C:\Users\Tushar\OneDrive\Documents\rag-chatbot\data"

def extract_text_from_txt(filename, chunk_size=500, overlap=50):
    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="windows-1252", errors="replace") as file:
            text = file.read()

    text = text.replace("\n", " ").replace("\r", " ").strip()

    # Split into sentences 
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    if overlap > 0:
        final_chunks = []
        for i in range(0, len(chunks)):
            start = max(0, i - 1)
            merged_chunk = " ".join(chunks[start:i+1])
            final_chunks.append(merged_chunk)
        return final_chunks
    else:
        return chunks
