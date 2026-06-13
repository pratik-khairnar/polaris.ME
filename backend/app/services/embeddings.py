from sentence_transformers import SentenceTransformer
print("LOADING EMBEDDING MODEL")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("EMBEDDING MODEL LOADED")
def generate_embeddings(chunks):
    
    embeddings = model.encode(chunks)

    return embeddings

if __name__ == "__main__":

    sample_chunks = [
        "Authentication uses JWT",
        "Frontend built using React"
    ]

    vectors = generate_embeddings(sample_chunks)

    print(vectors.shape)