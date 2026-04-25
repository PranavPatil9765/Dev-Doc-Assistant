# app/routes/session.py
from fastapi import APIRouter
import uuid
import time

from app.db.session_store import sessions, session_meta

router = APIRouter()

SESSION_TTL = 1800  # 30 mins

@router.post("/api/create-session")
def create_session():
    session_id = str(uuid.uuid4())

    sessions[session_id] = None  # no data yet
    session_meta[session_id] = time.time()

    return {"session_id": session_id}