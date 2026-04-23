# app/routes/query.py
from fastapi import APIRouter
from pydantic import BaseModel

from app.db.vector_store import get_vector_store
from app.services.retrieval_service import retrieve_docs
from app.services.llm_service import stream_answer
from fastapi.responses import StreamingResponse
router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_docs(request: QueryRequest):
    db = get_vector_store()
    
    if not db:
        return {"error": "No documents uploaded"}

    docs = retrieve_docs(db, request.query)

    return StreamingResponse(
        stream_answer(docs, request.query),
        media_type="text/plain"
    )