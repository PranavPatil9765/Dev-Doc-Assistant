# app/routes/upload.py
from fastapi import APIRouter, UploadFile
import shutil

from app.ingestion.parser import load_pdf
from app.services.embedding_service import create_chunks, get_embeddings
from app.db.vector_store import create_vector_store
from app.ingestion.code_parser import parse_code

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile):
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # File type handling
    filename = file.filename or ""
    if filename.endswith(".py"):
        docs = parse_code(file_path)
    elif filename.endswith(".pdf"):
        docs = load_pdf(file_path)
    else:
        return {"error": "Unsupported file type"}

    # Metadata merge
    for doc in docs:
        doc.metadata = {
            **doc.metadata,
            "source": filename,
            "page": doc.metadata.get("page", "unknown")
        }

    chunks = create_chunks(docs)
    embeddings = get_embeddings()
    
    create_vector_store(chunks, embeddings)

    return {"message": "File processed successfully"}