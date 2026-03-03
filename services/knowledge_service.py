from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.get("/search")
async def search_legal_acts(query: str, db: Session = Depends(get_db)):
    # Very rudimentary search matching across titles and sections
    results = db.query(models.LegalKnowledge).filter(
        (models.LegalKnowledge.title.contains(query)) |
        (models.LegalKnowledge.description.contains(query)) |
        (models.LegalKnowledge.section.contains(query))
    ).limit(3).all()
    
    if not results:
        return {"results": [{"section": "General", "description": "Please consult a recognized legal practitioner for more specific acts."}]}
        
    return {"results": [{"section": r.section, "title": r.title, "description": r.description} for r in results]}
