from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import List
import time
import os

from app.ingestion.parser import load_pdf, load_text, load_docx
from app.ingestion.code_parser import parse_code
from app.services.embedding_service import create_chunks, get_embeddings
from app.db.vector_store import create_vector_store
from app.db.session_store import sessions, session_meta
from app.db.cleanup import cleanup_sessions 

router = APIRouter()

# File type mappings
TEXT_EXTENSIONS = {".txt", ".md", ".markdown"}
DOCX_EXTENSIONS = {".docx"}
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".h",
    ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".scala", ".sh",
    ".bash", ".zsh", ".sql", ".html", ".css", ".scss", ".json", ".yaml",
    ".yml", ".xml", ".toml", ".ini", ".cfg"
}


def get_file_loader(filename: str, content):
    """Determine the appropriate loader based on file extension."""
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == ".pdf":
        return load_pdf, "pdf"
    elif ext in TEXT_EXTENSIONS:
        return load_text, "text"
    elif ext in DOCX_EXTENSIONS:
        return load_docx, "docx"
    elif ext in CODE_EXTENSIONS:
        return parse_code, "code"
    else:
        return None, None


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
            content = file.file.read()
            
            loader, file_type = get_file_loader(filename, content)
            
            if loader is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {filename}"
                )
            
            if file_type == "code":
                docs = loader(content.decode("utf-8"))
            else:
                # pdf, text, docx all accept bytes
                docs = loader(content)
            
            for doc in docs:
                doc.metadata = {
                    **doc.metadata,
                    "source": filename,
                    "page": doc.metadata.get("page", "unknown")
                }

            all_docs.extend(docs)

        except HTTPException:
            raise
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