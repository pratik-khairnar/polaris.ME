import os
from urllib import response
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question, retrieved_chunks):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
    Answer the question using ONLY the provided context.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

if __name__ == "__main__":

    chunks = [
        "Authentication is using the JWT.",
        "Token validity is 24 hours."
    ]

    answer = generate_answer(
        "How does authentication work?",
        chunks
    )

    print(answer)