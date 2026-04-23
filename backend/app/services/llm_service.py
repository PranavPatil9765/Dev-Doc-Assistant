# app/services/llm_service.py
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def generate_answer(context, query):
    combined_context = "\n".join([doc.page_content for doc in context])
    
    prompt = f"""
    Answer the question using the context below:
    
    Context:
    {combined_context}
    
    Question:
    {query}
    """
    
    response = llm.invoke(prompt)
    return response.content