from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from services.knowledge_service import search_legal_acts
from services.nlp_service import generate_completion, PromptRequest

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/query")
async def send_query(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. Look up any related acts
    legal_context_res = await search_legal_acts(query=req.query, db=db)
    acts = legal_context_res.get("results", [])
    
    # Format context for AI
    context_str = "\n".join([f"({a['section']}): {a['description']}" for a in acts])
    
    # 2. Ask Gemini! Provide the context we just searched
    nlp_req = PromptRequest(prompt=req.query, context=context_str)
    ai_response = await generate_completion(nlp_req)
    
    reply = ai_response.get("nlp_output", "")
    
    # Optionally store the ChatHistory in db (Skipped for brevity)
    
    return {
        "response": reply,
        "legal_context_found": [a["section"] for a in acts]
    }
