# app/services/embedding_service.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
def create_chunks(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_documents(documents)

def get_embeddings():
     return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")