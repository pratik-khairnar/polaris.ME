import chromadb
import uuid

print("INITIALIZING CHROMADB")

client = chromadb.PersistentClient(path="chroma_db")
print("CHROMADB CLIENT READY")

collection = client.get_or_create_collection(
    name="documents"
)

print("COLLECTION READY")

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
