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
    You are Polaris.ME, an AI-powered documentation and codebase intelligence assistant.

    Your task is to answer questions strictly using the provided context.

    Rules:

    1. Use ONLY information present in the context.
    2. Do NOT invent, assume, or hallucinate information.
    3. If the answer is not present in the context, respond with:
       "I couldn't find this information in the indexed documents."
    4. Be concise but complete.
    5. When discussing code, explain the purpose and behavior clearly.
    6. If multiple sources contribute to the answer, combine the information logically.
    7. Prefer technical accuracy over verbosity.
    
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
