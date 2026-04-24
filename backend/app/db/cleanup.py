import time
from app.db.session_store import sessions, session_meta

SESSION_TTL = 1800  # 30 mins

def cleanup_sessions():
    now = time.time()

    expired = [
        sid for sid, last_used in session_meta.items()
        if now - last_used > SESSION_TTL
    ]

    for sid in expired:
        sessions.pop(sid, None)
        session_meta.pop(sid, None)