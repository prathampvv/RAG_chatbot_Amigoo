from langchain_community.vectorstores import FAISS

def save_vector_db(db):
    db.save_local("C:/Users/Tushar/OneDrive/Documents/rag-chatbot/vectordb/faiss_index")

def load_vector_db(embeddings):
    return FAISS.load_local(
        folder_path="C:/Users/Tushar/OneDrive/Documents/rag-chatbot/vectordb/faiss_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
