# notebooks/01_chunk_text.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.document_processor import load_and_clean_text, chunk_text, save_chunks

# ✅ Corrected to use a folder path
text = load_and_clean_text("document.txt")

# ✅ Optional: Save full text
with open("document.txt", "w", encoding="utf-8") as f:
    f.write(text)

# ✅ Chunk the text
chunks = chunk_text(text)

# ✅ Save chunks
save_chunks(chunks, "chunks.txt")
print("chunks created")
