# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File
from typing import List
import shutil
import os

from app.ingestion.parser import load_pdf
from app.ingestion.code_parser import parse_code
from app.services.embedding_service import create_chunks, get_embeddings
from app.db.vector_store import create_vector_store

router = APIRouter()

@router.post("/upload")
async def upload_file(files: List[UploadFile] = File(...)):
    
    all_docs = []

    for file in files:
        file_path = f"temp_{file.filename}"

        # save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        filename = file.filename or ""

        try:
            # parse
            if filename.endswith(".py"):
                docs = parse_code(file_path)
            elif filename.endswith(".pdf"):
                docs = load_pdf(file_path)
            else:
                continue

            # metadata
            for doc in docs:
                doc.metadata = {
                    **doc.metadata,
                    "source": filename,
                    "page": doc.metadata.get("page", "unknown")
                }

            all_docs.extend(docs)

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    if not all_docs:
        return {"error": "No valid files uploaded"}

    chunks = create_chunks(all_docs)
    embeddings = get_embeddings()

    create_vector_store(chunks, embeddings)

    return {
        "message": "Files processed successfully",
        "files_processed": len(files)
    }