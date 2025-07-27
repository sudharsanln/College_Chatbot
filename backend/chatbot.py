import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import traceback 
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from fastapi.responses import HTMLResponse
from typing import List

# Setup
app=FastAPI()

@app.get("/", response_class=HTMLResponse)

def root():
    return """
    <html>
        <head><title>College Chatbot API</title></head>
        <body>
            <h2>College Chatbot API is running!</h2>
            <p>Use the <code>/chat</code> endpoint to ask questions.</p>
        </body>
    </html>
    """

@app.get("/favicon.ico")
def favicon():
    return {}

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Initialize embedding and load vector store
embedding_model = OllamaEmbeddings(model="nomic-embed-text")
db = FAISS.load_local(r"C:\\Users\\USER\\Documents\\ollamamodel\\college-index", embedding_model, allow_dangerous_deserialization=True)

# Load TinyLlama model
llm = OllamaLLM(model="tinyllama", temperature=0.2, max_tokens=150)

#Prompt Template
prompt = PromptTemplate.from_template("""
You are a friendly, smart and concise assistant.
When answering, speak naturally and helpfully. Avoid repeating or rephrasing the question. 
Keep your answer short and to the point.

Context:
{context}

User's Question:
{question}

Your Answer:
""")


# Build RetrievalQA pipeline
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=db.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt}
)

# Request Schema
class ChatRequest(BaseModel):
    query:str 

class ChatResponse(BaseModel):
    success:bool
    result:str | None=None
    error: str | None=None

class DiveDeeperRequest(BaseModel):
    previous_answer: str

# API Endpoint for dive deeper
@app.post("/dive_deeper")
async def dive_deeper(request: DiveDeeperRequest):
    try:
        followup = f"Can you elaborate further on: {request.previous_answer}"
        result = qa_chain.invoke({"query": followup})
        return {"success": True, "answer": result["result"]}
    except Exception as e:
        return {"success": False, "error": str(e)}

# API Endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        result = qa_chain.invoke({"query": request.query})
        return {"success": True, "result": result["result"]}
    
    except Exception as e:
        traceback.print_exc()
        return {"success": False, "error": f"An error occurred: {str(e)}"}


'''
# Chatbot loop
def chatbot():
    print("\nChatbot(Type 'exit' to quit)")
    while True:
        query = input("Ask a question: ")
        if query.lower() in ["exit", "quit"]:
            break
        try :
            result = qa_chain.invoke({"query":query})
            print("\nBot:", result["result"])
        
        except Exception as e:
            print("Error", e)

        print("-" * 50)

if __name__ == "__main__":
    chatbot()


#Alt root/API Endpoint
def root():
    return {"message": "College Chatbot API is running; use /chat to ask questions."}
'''