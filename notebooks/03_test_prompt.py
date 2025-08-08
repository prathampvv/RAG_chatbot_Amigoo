import sys
import os

# Add root project path to import custom modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.document_processor import extract_text_from_txt

# Use full path to the file in 'data' directory
txt_path = r"C:\Users\Tushar\OneDrive\Documents\rag-chatbot\data\document.txt"
chunks = extract_text_from_txt(txt_path)

# Print a few chunks to verify
for i, chunk in enumerate(chunks[:3]):
    print(f"Chunk {i+1}:\n{chunk}\n{'='*40}")
