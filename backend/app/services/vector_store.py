import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

def store_chunks(chunks, embeddings):

    ids = []

    for i in range(len(chunks)):
        ids.append(str(i))

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids
    )

def clear_collection():

    global collection

    client.delete_collection("documents")

    collection = client.get_or_create_collection(
        name="documents"
    )


from app.services.embeddings import generate_embeddings

if __name__ == "__main__":

    chunks = [
        "Authentication uses JWT",
        "Frontend built using React"
    ]

    vectors = generate_embeddings(chunks)

    store_chunks(chunks, vectors)

    print("Stored successfully")
    print(collection.count())