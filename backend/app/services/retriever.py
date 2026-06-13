from app.services.vector_store import collection
from app.services.embeddings import model


def retrieve_chunks(query, n_results=3):

    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results["documents"][0]

if __name__ == "__main__":

    query = "How does authentication work?"

    docs = retrieve_chunks(query)

    print(docs)