# app/routes/query.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time

from app.db.session_store import sessions, session_meta
from app.db.cleanup import cleanup_sessions
from app.services.retrieval_service import retrieve_docs
from app.services.llm_service import stream_answer

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    session_id: str


@router.post("/api/query")
async def query_docs(request: QueryRequest):
    cleanup_sessions()

    if request.session_id not in sessions:
        return {"error": "Invalid session"}

    if sessions[request.session_id] is None:
        return {"error": "No documents uploaded in this session"}

    db = sessions[request.session_id]

    session_meta[request.session_id] = time.time()

    docs = retrieve_docs(db, request.query)

    return StreamingResponse(
        stream_answer(docs, request.query),
    )