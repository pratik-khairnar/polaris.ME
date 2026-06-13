from fastapi import APIRouter

from app.models.schemas import ChatRequest
from app.services.retriever import retrieve_chunks
from app.services.llm import generate_answer

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    chunks = retrieve_chunks(request.question)

    answer = generate_answer(
        request.question,
        chunks
    )

    return {
        "answer": answer
    }