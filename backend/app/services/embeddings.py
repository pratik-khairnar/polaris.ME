from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

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