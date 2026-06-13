from fastapi import APIRouter, BackgroundTasks
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import GithubRequest
from app.services.github_loader import load_github_repo
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings
from app.services.vector_store import store_chunks

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=4)

@router.post("/github")
async def ingest_github_repo(request: GithubRequest):
    loop = asyncio.get_event_loop()
    
    # Run the blocking file load in an executor
    files = await loop.run_in_executor(executor, load_github_repo, request.repo_url)

    files_indexed = 0

    for file in files:
        # Chunks are usually light enough to stay here, or delegate if they are huge
        chunks = chunk_text(file["content"])

        if not chunks:
            continue

        # Delegate heavy embedding generation to thread pool
        embeddings = await loop.run_in_executor(
            executor, generate_embeddings, chunks
        )

        # Delegate DB storage
        await loop.run_in_executor(
            executor, 
            store_chunks, 
            chunks, 
            embeddings, 
            file["relative_path"]  # Use the relative path for metadata
        )

        files_indexed += 1

    return {
        "message": "Repository indexed successfully",
        "files_indexed": files_indexed
    }