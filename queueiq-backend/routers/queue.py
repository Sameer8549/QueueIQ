from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

router = APIRouter(prefix="/api/queue", tags=["queue"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/patient")
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    existing = crud.get_patient_by_whatsapp(db, patient.whatsapp_number)
    if existing:
        return {"id": existing.id, "whatsapp_number": existing.whatsapp_number, "message": "Patient already registered"}
    
    db_patient = crud.create_patient(db, patient)
    return {"id": db_patient.id, "whatsapp_number": db_patient.whatsapp_number, "message": "Patient registered successfully"}

@router.post("/token")
def create_token(token: schemas.TokenCreate, db: Session = Depends(get_db)):
    db_token = crud.create_token(db, token)
    return {
        "id": db_token.id,
        "token_number": db_token.token_number,
        "patient_id": db_token.patient_id,
        "department": db_token.department,
        "estimated_wait_time_mins": db_token.estimated_wait_time_mins,
        "queue_position": db_token.queue_position,
        "status": db_token.status.value,
        "message": f"Token {db_token.token_number} created — estimated wait {db_token.estimated_wait_time_mins} minutes"
    }

@router.get("/active")
def get_active_queue(db: Session = Depends(get_db)):
    tokens = crud.get_active_tokens(db)
    return [{
        "id": t.id,
        "patient_id": t.patient_id,
        "token_number": t.token_number,
        "status": t.status.value,
        "department": t.department,
        "chief_complaint": t.chief_complaint,
        "symptoms_text": t.symptoms_text,
        "severity": t.severity,
        "extracted_symptoms": t.extracted_symptoms,
        "duration": t.duration,
        "red_flags": t.red_flags,
        "estimated_wait_time_mins": t.estimated_wait_time_mins,
        "queue_position": t.queue_position,
        "created_at": str(t.created_at)
    } for t in tokens]
