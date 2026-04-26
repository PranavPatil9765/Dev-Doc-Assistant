# app/ingestion/parser.py
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from typing import Union, IO
from io import BytesIO
import tempfile


def load_pdf(file):
    """Load PDF files from file path, bytes, or IO object."""
    if isinstance(file, str):
        # File path
        loader = PyPDFLoader(file)
    elif isinstance(file, bytes):
        # Bytes content - write to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf", mode="wb") as temp_file:
            temp_file.write(file)
            temp_file_path = temp_file.name
        loader = PyPDFLoader(temp_file_path)
    else:
        # IO object (e.g., UploadFile)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.read())
            file.seek(0)  # Reset file position
            temp_file_path = temp_file.name
        loader = PyPDFLoader(temp_file_path)

    documents = loader.load()
    return documents


def load_text(content):
    """Load text files (txt, md, markdown) from bytes or str."""
    if isinstance(content, str):
        # Already a string - create temp file with content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
    else:
        # Bytes content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name

    loader = TextLoader(temp_file_path, encoding="utf-8")
    return loader.load()


def load_docx(content):
    """Load DOCX files from bytes or str."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", mode="wb") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    loader = Docx2txtLoader(temp_file_path)
    return loader.load()