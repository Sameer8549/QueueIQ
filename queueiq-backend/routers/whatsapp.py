from fastapi import APIRouter, Depends, BackgroundTasks, Form
from sqlalchemy.orm import Session
from database import get_db
from ai_engine import AIEngine
import models, crud
import json

router = APIRouter(prefix="/webhook", tags=["whatsapp"])

@router.post("/whatsapp")
async def whatsapp_webhook(
    background_tasks: BackgroundTasks,
    From: str = Form(""),
    Body: str = Form(""),
    MediaUrl0: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    Twilio-compatible WhatsApp webhook
    Processes voice notes: transcribe → extract symptoms → triage
    """
    if MediaUrl0:
        # Process audio in background
        background_tasks.add_task(process_audio_triage, MediaUrl0, From, db)
    
    return {"status": "received", "message": "Processing your symptoms..."}


async def process_audio_triage(media_url: str, sender: str, db: Session):
    """Full AI pipeline via Gemini Cloud"""
    
    # 1. Transcribe and Translate
    # Since we don't have the language_code here, we assume English/Auto
    english_text, original_text = await AIEngine.transcribe_and_translate(media_url, "en")
    
    # 2. Find latest token for this phone number
    token = db.query(models.Token).filter(
        models.Token.phone_number.contains(sender.replace("whatsapp:", ""))
    ).order_by(models.Token.created_at.desc()).first()
    
    if token:
        # 3. Generate Clinical Summary & Triage
        triage = await AIEngine.get_emergency_triage(token.token_number, token.age, english_text, "")
        summary = await AIEngine.generate_clinical_summary(token.token_number, token.age, token.gender, english_text, "")
        
        # 4. Update the token
        update_data = {
            "transcription": english_text,
            "clinical_summary": summary.get("summary"),
            "patient_brief": summary.get("patient_brief"),
            "emergency_risk": triage,
            "status": "emergency-routed" if triage.get("is_emergency") else "waiting"
        }
        
        crud.update_token_symptoms(db, token.id, update_data)
        
        # 5. Send confirmation back
        conf_msg = f"Summary Received: {summary.get('summary', {}).get('dashboard_headline', 'Symptoms processed.')}"
        if triage.get("is_emergency"):
            conf_msg = f"⚠️ Alert: {triage.get('patient_whatsapp_message', 'Emergency detected. Staff notified.')}"
            
        await AIEngine.send_whatsapp_message(sender, conf_msg)
    
    return
