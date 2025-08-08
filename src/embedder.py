from langchain_community.embeddings import HuggingFaceEmbeddings

def embed_chunks(chunks):
    # Create the correct embeddings object
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Return it (second return value can be None if not needed)
    return embedding_model, None
