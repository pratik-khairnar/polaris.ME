from fastapi import APIRouter, UploadFile, File
from app.services.document_loader import load_document
from app.services.chunker import chunk_text
from app.services.embeddings import generate_embeddings
from app.services.vector_store import store_chunks
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
        
    text = load_document(file_path)

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    store_chunks(
        chunks,
        embeddings
    )

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "preview": text[:200]
    }