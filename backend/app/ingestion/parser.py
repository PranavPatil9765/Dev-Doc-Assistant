# app/ingestion/parser.py
from langchain_community.document_loaders import PyPDFLoader
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