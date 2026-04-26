import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings

def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

def get_embeddings():
    cohere_api_key = os.getenv("COHERE_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY not found in environment variables")

    return CohereEmbeddings(  # type: ignore
        model="embed-english-v3.0",
        cohere_api_key=cohere_api_key,
        user_agent="my-app" 
    )