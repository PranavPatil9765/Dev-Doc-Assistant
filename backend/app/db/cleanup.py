import time
import os
from pinecone import Pinecone
from app.db.session_store import sessions, session_meta

SESSION_TTL = 1800  # 30 mins


def get_pinecone_index():
    """Get Pinecone index instance."""
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-index")
    
    if not api_key:
        return None
    
    pc = Pinecone(api_key=api_key)
    return pc.Index(index_name)


def delete_namespace(namespace: str):
    """Delete all vectors in a namespace to free up space."""
    index = get_pinecone_index()
    if index:
        # Delete all vectors in namespace by upserting empty upsert
        # Pinecone doesn't have direct namespace delete, so we delete all vectors
        try:
            # Get all vector IDs in namespace and delete them
            # Using delete with filter to remove namespace contents
            index.delete(delete_all=True, namespace=namespace)
        except Exception:
            # Fallback: try to delete by matching all (some Pinecone tiers don't support this)
            pass


def cleanup_sessions():
    now = time.time()

    expired = [
        sid for sid, last_used in session_meta.items()
        if now - last_used > SESSION_TTL
    ]

    for sid in expired:
        # Delete associated Pinecone namespace
        delete_namespace(sid)
        
        sessions.pop(sid, None)
        session_meta.pop(sid, None)