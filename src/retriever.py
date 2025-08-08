def search_similar_chunks(query, embedding_model, chunks, index, top_k=3):
    docs_and_scores = index.similarity_search_with_score(query, k=top_k)
    top_chunks = [doc.page_content for doc, _ in docs_and_scores]
    return top_chunks
