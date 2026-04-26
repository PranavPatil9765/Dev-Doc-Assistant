# app/ingestion/parser.py
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from typing import Union, IO
from io import BytesIO
import tempfile


def load_pdf(file: Union[str, IO]):
    if isinstance(file, str):
        loader = PyPDFLoader(file)
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.read())
            temp_file_path = temp_file.name

        loader = PyPDFLoader(temp_file_path)

    documents = loader.load()
    return documents


def load_text(content: bytes):
    """Load text files (txt, md, markdown)."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="wb") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    loader = TextLoader(temp_file_path, encoding="utf-8")
    return loader.load()


def load_docx(content: bytes):
    """Load DOCX files."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", mode="wb") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    loader = Docx2txtLoader(temp_file_path)
    return loader.load()