from fastapi import APIRouter, Depends, BackgroundTasks, Form
from sqlalchemy.orm import Session
from database import SessionLocal
import ai_engine
import emergency_triage
import education_engine
import crud
import json

router = APIRouter(prefix="/webhook", tags=["whatsapp"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/whatsapp")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    From: str = Form(""),
    Body: str = Form(""),
    MediaUrl0: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Twilio-compatible WhatsApp webhook (PRD Module 2 + 4)
    Processes voice notes: transcribe → extract symptoms → triage → educate
    """
    if MediaUrl0:
        # Process audio in background
        background_tasks.add_task(process_audio_triage, MediaUrl0, From, db)
    
    return {"status": "received", "message": "Processing your symptoms..."}


def process_audio_triage(media_url: str, sender: str, db: Session):
    """Full AI pipeline: Whisper → BioBERT NER → Triage → Education"""
    
    # Step 1: Transcribe (simulating Whisper)
    transcription = ai_engine.transcribe_audio(media_url)
    
    # Step 2: Extract symptoms (simulating BioBERT NER)
    extraction = ai_engine.extract_symptoms(transcription)
    
    # Step 3: Emergency triage check
    triage_result = emergency_triage.check_emergency(transcription)
    
    # Step 4: Generate health education brief
    health_brief = education_engine.generate_health_brief(
        extraction["symptoms"],
        language="en"
    )
    
    # Step 5: Find patient's latest token and update it
    patient = crud.get_patient_by_whatsapp(db, sender)
    if patient:
        tokens = db.query(crud.models.Token).filter(
            crud.models.Token.patient_id == patient.id,
            crud.models.Token.status.in_([
                crud.models.TokenStatus.waiting,
                crud.models.TokenStatus.in_progress
            ])
        ).order_by(crud.models.Token.created_at.desc()).first()
        
        if tokens:
            update_data = {
                "chief_complaint": extraction["chief_complaint"],
                "symptoms_text": transcription,
                "severity": extraction["severity"],
                "department": extraction["department"],
                "extracted_symptoms": extraction["extracted_symptoms_json"],
                "red_flags": extraction["red_flags_json"],
                "duration": extraction["duration"],
            }
            
            if triage_result["is_emergency"]:
                update_data["status"] = crud.models.TokenStatus.emergency
            
            crud.update_token_symptoms(db, tokens.id, update_data)
    
    return {
        "transcription": transcription,
        "extraction": extraction,
        "triage": triage_result,
        "health_brief": health_brief
    }

@router.get("/simulate-intake")
def simulate_intake(token_id: int = 1, db: Session = Depends(get_db)):
    """Quick demo endpoint: simulates a patient voice note being processed"""
    transcription = ai_engine.transcribe_audio("demo")
    extraction = ai_engine.extract_symptoms(transcription)
    triage = emergency_triage.check_emergency(transcription)
    brief = education_engine.generate_health_brief(extraction["symptoms"])
    
    # Update the token
    crud.update_token_symptoms(db, token_id, {
        "chief_complaint": extraction["chief_complaint"],
        "symptoms_text": transcription,
        "severity": extraction["severity"],
        "department": extraction["department"],
        "extracted_symptoms": extraction["extracted_symptoms_json"],
        "red_flags": extraction["red_flags_json"],
        "duration": extraction["duration"],
        "status": crud.models.TokenStatus.emergency if triage["is_emergency"] else None
    })
    
    return {
        "transcription": transcription,
        "extraction": extraction,
        "triage": triage,
        "health_brief": brief
    }
