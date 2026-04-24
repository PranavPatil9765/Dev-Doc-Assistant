# app/db/vector_store.py
from langchain_community.vectorstores import FAISS
db = None

def create_vector_store(chunks, embeddings):
    global db
    db = FAISS.from_documents(chunks, embeddings)
    return db