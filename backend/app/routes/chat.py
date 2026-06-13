from fastapi import APIRouter

from app.models.schemas import ChatRequest
from app.services.hybrid_search import hybrid_search
from app.services.llm import generate_answer

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    retrieved_docs = hybrid_search(request.question)

    answer = generate_answer(request.question, retrieved_docs)

    return {"answer": answer, "sources": []}