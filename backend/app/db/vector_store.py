# app/db/vector_store.py
from pinecone import Pinecone, ServerlessSpec
import os
import uuid

db = None

def create_vector_store(chunks, embeddings):
    global db
    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-index")
    
    if not api_key:
        raise ValueError("PINECONE_API_KEY not set")
    
    pc = Pinecone(api_key=api_key)
    
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
    
    index = pc.Index(index_name)
    
    # Manually embed and upsert documents
    if chunks:
        records = []
        for i, chunk in enumerate(chunks):
            # Get embedding for the chunk content
            text = chunk.page_content
            embedding = embeddings.embed_query(text)
            
            records.append({
                "id": str(uuid.uuid4()),
                "values": embedding,
                "metadata": {
                    "text": text,
                    "source": chunk.metadata.get("source", "unknown"),
                    "page": chunk.metadata.get("page", "unknown")
                }
            })
        
        # Upsert in batches
        index.upsert(vectors=records, namespace="default")
    
    # Store index reference for similarity search
    db = index
    return db