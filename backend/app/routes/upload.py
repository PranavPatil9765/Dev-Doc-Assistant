# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import shutil
import os
import time

from app.ingestion.parser import load_pdf
from app.ingestion.code_parser import parse_code
from app.services.embedding_service import create_chunks, get_embeddings
from app.db.vector_store import create_vector_store
from app.db.session_store import sessions, session_meta
from app.db.cleanup import cleanup_sessions 

router = APIRouter()

@router.post("/api/upload")
async def upload_file(
    session_id: str = Query(...), 
    files: List[UploadFile] = File(...)
):
    cleanup_sessions()

    if session_id not in sessions:
        return {"error": "Invalid session"}

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

    if not chunks:
        return {"error": "No valid content extracted from files"}
    
    embeddings = get_embeddings()

    db = create_vector_store(chunks, embeddings)
    sessions[session_id] = db

    session_meta[session_id] = time.time()

    return {
        "message": "Files processed successfully",
        "files_processed": len(files),
        "session_id": session_id
    }