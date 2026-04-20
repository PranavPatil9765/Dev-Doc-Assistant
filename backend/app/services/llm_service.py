# app/services/llm_service.py
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(temperature=0)

def generate_answer(context, query):
    combined_context = "\n".join([doc.page_content for doc in context])
    
    prompt = f"""
    Answer the question using the context below:
    
    Context:
    {combined_context}
    
    Question:
    {query}
    """
    
    return llm.predict(prompt)