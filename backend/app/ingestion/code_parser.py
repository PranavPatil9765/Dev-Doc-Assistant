import re
from langchain_core.documents import Document
def parse_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    # split by functions (simple regex)
    functions = re.split(r"\ndef ", code)

    docs = []
    for func in functions:
        if func.strip():
            docs.append(
                Document(
                    page_content=func,
                    metadata={"type": "function"}
                )
            )
    return docs