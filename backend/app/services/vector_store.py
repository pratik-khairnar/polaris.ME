import chromadb
import uuid

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

def store_chunks(chunks, embeddings, filename):

    ids = []
    metadatas = []

    for i in range(len(chunks)):
        ids.append(str(uuid.uuid4()))
        metadatas.append({
            "source": filename
        })

    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids,
        metadatas=metadatas
    )

def clear_collection():

    global collection

    client.delete_collection("documents")

    collection = client.get_or_create_collection(
        name="documents"
    )


from app.services.embeddings import generate_embeddings
