from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent
app = FastAPI(title="Agentic AI Assistant")
class ChatRequest(BaseModel):
    message: str
class ChatResponse(BaseModel):
    reply: str


@app.get("/")
def health_check():
    return {"status": "agent is running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply_text = run_agent(request.message)
    return ChatResponse(reply=reply_text)
