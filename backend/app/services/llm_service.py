# app/services/llm_service.py
from langchain_groq import ChatGroq
from typing import AsyncGenerator
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    streaming=True 
)

async def stream_answer(context, query) -> AsyncGenerator[str, None]:
    combined_context = "\n".join([doc.page_content for doc in context])

    prompt = f"""
    Answer ONLY using the context.
    If not found, say "Not found in provided documents".

    Context:
    {combined_context}

    Question:
    {query}
    """

    # stream answer
    async for chunk in llm.astream(prompt):
        content = getattr(chunk, "content", "")

        if content:
            yield str(content)  
    yield "\n\nSources:\n"

    sources = list({
        f"{doc.metadata.get('source')} - page {doc.metadata.get('page')}"
        for doc in context
    })

    for src in sources:
        yield str(f"- {src}\n") 