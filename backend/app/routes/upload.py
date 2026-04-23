# app/routes/upload.py
from fastapi import APIRouter, UploadFile
import shutil

from app.ingestion.parser import load_pdf
from app.services.embedding_service import create_chunks, get_embeddings
from app.db.vector_store import create_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_pdf(file_path)
    for doc in docs:
        doc.metadata["source"] = file.filename
    chunks = create_chunks(docs)
    embeddings = get_embeddings()
    
    create_vector_store(chunks, embeddings)

    return {"message": "File processed successfully"}