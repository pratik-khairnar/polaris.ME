import numpy as np
from rank_bm25 import BM25Okapi
from app.services.vector_store import collection
from app.services.embeddings import model


def hybrid_search(query: str, n_results: int = 8) -> list:
    """Performs a Hybrid Search by merging Dense Vector embeddings (ChromaDB)

    and Sparse Keyword scores (BM25Okapi).
    """
    # 1. Dense Vector Search
    query_embedding = model.encode(query)
    vector_results = collection.query(
        query_embeddings=[query_embedding.tolist()], n_results=n_results
    )

    # Fetch safely nested list of documents from vector results
    vector_docs = (
        vector_results["documents"][0]
        if vector_results and vector_results["documents"]
        else []
    )

    # 2. Sparse Keyword Search (BM25)
    # WARNING: collection.get() pulls everything. For production polaris.ME,
    # consider persisting BM25 indices or scoping this to a specific repository ID.
    all_docs = collection.get()
    documents = all_docs.get("documents", [])

    if not documents:
        return vector_docs[:n_results]

    # Tokenize corpus and query for BM25 processing
    tokenized_docs = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)

    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)

    # Extract top indices based on highest BM25 score
    ranked_indices = sorted(
        range(len(scores)), key=lambda i: scores[i], reverse=True
    )[:n_results]

    bm25_docs = [documents[i] for i in ranked_indices]

    # 3. Reciprocal Union & Deduplication
    combined_docs = []

    # Prioritize semantic vector matches first, then append keyword matches
    for doc in vector_docs:
        if doc not in combined_docs:
            combined_docs.append(doc)

    for doc in bm25_docs:
        if doc not in combined_docs:
            combined_docs.append(doc)

    return combined_docs[:n_results]