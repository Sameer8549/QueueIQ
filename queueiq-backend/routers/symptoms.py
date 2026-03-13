from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from ai_engine import AIEngine
import datetime
import shutil
import os

router = APIRouter(prefix="/api/v1/symptoms", tags=["symptoms"])

@router.get("/summaries/today")
async def get_summaries_today(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    tokens = db.query(models.Token).filter(
        models.Token.created_at >= start_of_day,
        models.Token.clinical_summary != None
    ).all()
    
    return [
        {
            "token_number": t.token_number,
            "patient_name_masked": t.patient_name_masked,
            "language_code": t.language_code,
            "summary": t.clinical_summary
        } for t in tokens
    ]

@router.post("/voice-assessment")
async def voice_assessment(token_number: str, audio: UploadFile = File(...), db: Session = Depends(get_db)):
    token = db.query(models.Token).filter(models.Token.token_number == token_number).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
        
    # Save temporary audio file
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = f"{temp_dir}/{token_number}_{audio.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
        
    # AI Pipeline: ASR -> TRANSLATE -> SUMMARY -> TRIAGE
    try:
        # 1. Transcription & Translation
        english_complaint, original_text = await AIEngine.transcribe_and_translate(file_path, token.language_code)
        
        # 2. Dual Clinical & Patient Summary
        ai_output = await AIEngine.generate_clinical_summary(
            token_number=token.token_number,
            age=token.age or 35,
            gender=token.gender or "Unknown",
            transcription=english_complaint,
            conditions="None"
        )
        
        # 3. Emergency Triage
        triage = await AIEngine.get_emergency_triage(
            token=token.token_number,
            age=token.age or 35,
            transcription=english_complaint,
            conditions="None"
        )
        
        # Update token record
        token.transcription = english_complaint
        token.clinical_summary = ai_output.get("summary")
        token.patient_brief = ai_output.get("patient_brief")
        token.emergency_risk = triage
        
        if triage.get("is_emergency"):
            token.status = "emergency-routed"
        
        db.commit()
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {
            "transcription": original_text,
            "transcription_english": english_complaint,
            "summary": ai_output.get("summary"),
            "patient_brief": ai_output.get("patient_brief"),
            "triage": triage
        }
        
    except Exception as e:
        print(f"AI Pipeline Failed: {e}")
        raise HTTPException(status_code=500, detail="Symptom assessment failed")
