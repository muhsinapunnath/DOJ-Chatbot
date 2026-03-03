from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
import os

router = APIRouter()

# API Keys would normally be in a .env file, assuming mocking if not present
GENAI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBGlxImLD_sIUTB6E6pdKXzBUXgAeCBjlQ")

class PromptRequest(BaseModel):
    prompt: str
    context: str = ""
    
@router.post("/generate")
async def generate_completion(req: PromptRequest):
    if not GENAI_KEY:
        # Mock mode fallback if no key provided yet
        return {"nlp_output": f"Mock AI Response: Based on your query and the context provided ({req.context}), the relevant legal proceeding requires contacting a lawyer."}
        
    try:
        genai.configure(api_key=GENAI_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        full_prompt = f"You are an AI legal assistant for the Department of Justice. Use the provided context to inform your answer if relevant, and rely on your expansive general legal knowledge to thoroughly answer the query.\nContext: {req.context}\nQuery: {req.prompt}\nAnswer formally, courteously, and helpfully:"
        
        response = model.generate_content(full_prompt)
        return {"nlp_output": response.text}
    except Exception as e:
        return {"nlp_output": f"AI Error: {str(e)}"}
