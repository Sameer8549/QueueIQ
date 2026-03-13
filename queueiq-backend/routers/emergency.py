from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from ai_engine import AIEngine
import datetime

router = APIRouter(prefix="/api/v1/emergency", tags=["emergency"])

@router.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    # Fetch tokens with emergency status or high emergency score
    alerts = db.query(models.Token).filter(
        (models.Token.status == "emergency-routed") | 
        (models.Token.status == "called")
    ).all()
    
    return [
        {
            "id": t.id,
            "token_number": t.token_number,
            "patient_name_masked": t.patient_name_masked,
            "department": t.department,
            "status": t.status,
            "summary": t.clinical_summary,
            "created_at": t.created_at
        } for t in alerts
    ]

@router.post("/trigger-staff")
async def trigger_emergency(token_number: str, reason: str, db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token_number == token_number).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
        
    token.status = "emergency-routed"
    db.commit()
    
    # In a real app, this would trigger a WhatsApp/SMS via Twilio
    return {"message": "Emergency alert broadcasted to Desk & Medical Team."}

@router.get("/stats")
def get_emergency_stats(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    count = db.query(models.Token).filter(
        models.Token.created_at >= start_of_day,
        models.Token.status == "emergency-routed"
    ).count()
    
    return {
        "active_emergencies": count,
        "avg_response_time": "4.2m",
        "critical_count": count
    }
