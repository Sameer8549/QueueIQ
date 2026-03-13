from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from ai_engine import AIEngine
import models, schemas
import datetime

router = APIRouter(prefix="/api/v1/queue", tags=["queue"])

@router.get("/live")
def get_live_queue(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    tokens = db.query(models.Token).filter(models.Token.created_at >= start_of_day).all()
    
    return {
        "tokens": [
            {
                "token_number": t.token_number,
                "patient_name_masked": t.patient_name_masked or "Unknown",
                "department": t.department or "General",
                "wait_min": 15, # Placeholder for logic
                "status": t.status
            } for t in tokens
        ]
    }

@router.post("/register")
def register_token(req: schemas.TokenCreate, db: Session = Depends(get_db)):
    hospital = db.query(models.Hospital).filter(models.Hospital.id == req.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    
    # Simple token generation logic for now (e.g., A-101)
    # real production would use a counter or department-specific sequence
    prefix = req.department[:1].upper() if req.department else "P"
    count = db.query(models.Token).count() + 1
    token_val = f"{prefix}-{100 + count}"
    
    new_token = models.Token(
        token_number=token_val,
        patient_name_masked=req.patient_name_masked,
        language_code=req.language_code,
        department=req.department,
        hospital_id=req.hospital_id,
        status="waiting"
    )
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return new_token

@router.get("/status/{token_number}")
def get_token_status(token_number: str, db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token_number == token_number).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
        
    return {
        "token_number": token.token_number,
        "queue_position": 8,
        "estimated_wait_min": 25,
        "estimated_wait_max": 35,
        "department": token.department or "General Medicine",
        "hospital_name": "Wenlock District Hospital",
        "called": token.status == "called"
    }

@router.post("/toggle-whatsapp")
async def toggle_whatsapp(token_number: str, enabled: bool, db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token_number == token_number).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
        
    token.whatsapp_enabled = enabled
    db.commit()
    
    if enabled:
        await AIEngine.send_whatsapp_message(
            token.phone_number, 
            f"✅ WhatsApp updates enabled for Token {token.token_number}. We'll notify you when your turn approaches."
        )
        
    return {"status": "success", "enabled": enabled}
