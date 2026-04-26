import re
from langchain_core.documents import Document


def parse_code(content: str):
    """Parse code content and split into document chunks."""
    if not content or not content.strip():
        return []

    # Add back 'def ' that was split off
    functions = re.split(r"\ndef ", content)

    docs = []
    for i, func in enumerate(functions):
        func = func.strip()
        if not func:
            continue

        # Prepend 'def ' to all but first chunk
        if i > 0:
            func = "def " + func

        if func:
            docs.append(
                Document(
                    page_content=func,
                    metadata={"type": "code"}
                )
            )

    return docs