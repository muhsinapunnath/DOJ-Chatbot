from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import database
import models

# Routers
from services import auth_service
from services import chat_service
from services import knowledge_service
from services import nlp_service

app = FastAPI(title="DOJ AI Legal Chatbot Gateway", version="1.0.0")

# Mount Static Files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include Routers representing microservices architecture mapping
app.include_router(auth_service.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat_service.router, prefix="/api/chat", tags=["Chat"])
app.include_router(knowledge_service.router, prefix="/api/knowledge", tags=["Legal Knowledge"])
app.include_router(nlp_service.router, prefix="/api/nlp", tags=["NLP / Gemini"])

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

