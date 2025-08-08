def build_prompt(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks)
    return f"""You are a helpful assistant. Answer based on the context.

Context:
{context}

Question: {query}
Answer:"""
