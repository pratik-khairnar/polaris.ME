from app.services.vector_store import collection
from app.services.embeddings import model


def retrieve_chunks(query, n_results=8):

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    print(results["metadatas"])
    
    return {
        "documents": results["documents"][0],
        "metadata": results["metadatas"][0]
    }
