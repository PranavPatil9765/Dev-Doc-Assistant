# app/services/retrieval_service.py
from langchain_cohere import CohereEmbeddings
import os

def retrieve_docs(db, query, namespace, k=3):
    # db is now a Pinecone Index object
    cohere_api_key = os.getenv("COHERE_API_KEY")
    embeddings = CohereEmbeddings( # type: ignore
        model="embed-english-v3.0",
        cohere_api_key=cohere_api_key,
        user_agent="my-app"
    )
    
    # Query the index - use session-specific namespace for isolation
    query_embedding = embeddings.embed_query(query)
    results = db.query(
        vector=query_embedding,
        top_k=k,
        include_metadata=True,
        namespace=namespace
    )
    
    # Convert results to documents-like format
    from langchain_core.documents import Document
    docs = []
    for match in results.matches:
        docs.append(Document(
            page_content=match.metadata.get("text", ""),
            metadata={
                "source": match.metadata.get("source", "unknown"),
                "page": match.metadata.get("page", "unknown")
            }
        ))
    
    return docs