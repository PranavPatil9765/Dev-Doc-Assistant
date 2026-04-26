from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import List
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
        raise HTTPException(
            status_code=404,
            detail="Invalid or expired session"
        )

    all_docs = []

    for file in files:
        filename = file.filename or ""

        try:
            if filename.endswith(".py"):
                docs = parse_code(file.file.read().decode("utf-8"))
            elif filename.endswith(".pdf"):
                docs = load_pdf(file.file)
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {filename}"
                )

            for doc in docs:
                doc.metadata = {
                    **doc.metadata,
                    "source": filename,
                    "page": doc.metadata.get("page", "unknown")
                }

            all_docs.extend(docs)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file {filename}: {str(e)}"
            )

    if not all_docs:
        raise HTTPException(
            status_code=400,
            detail="No valid files uploaded"
        )

    chunks = create_chunks(all_docs)

    if not chunks:
        raise HTTPException(
            status_code=422,
            detail="No extractable content found in files"
        )

    embeddings = get_embeddings()

    try:
        db = create_vector_store(chunks, embeddings, session_id)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Vector store creation failed: {str(e)}"
        )

    sessions[session_id] = db
    session_meta[session_id] = time.time()

    return {
        "message": "Files processed successfully",
        "files_processed": len(files),
        "session_id": session_id
    }