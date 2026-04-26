# app/db/vector_store.py
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone , ServerlessSpec
import os

db = None

def create_vector_store(chunks, embeddings):
    global db
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-index")
    
    # Create index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
            )
        )
    
    db = PineconeVectorStore.from_documents(
        chunks, 
        embeddings, 
        index_name=index_name
    )
    return db