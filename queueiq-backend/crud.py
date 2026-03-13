from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
import time
import random

DEPARTMENTS = ["General Medicine", "Pediatrics", "Orthopedics", "ENT", "Dermatology", "Cardiology", "Gynecology"]

def get_patient_by_whatsapp(db: Session, whatsapp_number: str):
    return db.query(models.Patient).filter(models.Patient.whatsapp_number == whatsapp_number).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def create_token(db: Session, token: schemas.TokenCreate):
    token_number = f"TK-{int(time.time()) % 10000}"
    
    # Count current queue to assign position
    active_count = db.query(models.Token).filter(
        models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.in_progress])
    ).count()
    
    # Simulate intelligent wait prediction (PRD Module 1)
    base_wait = 15 + (active_count * 8) + random.randint(-5, 10)
    
    db_token = models.Token(
        patient_id=token.patient_id,
        token_number=token_number,
        department=token.department or random.choice(DEPARTMENTS),
        chief_complaint=token.chief_complaint,
        estimated_wait_time_mins=max(10, base_wait),
        queue_position=active_count + 1,
        severity="normal"
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_active_tokens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Token).filter(
        models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.in_progress, models.TokenStatus.emergency])
    ).order_by(models.Token.created_at.desc()).offset(skip).limit(limit).all()

def get_emergency_tokens(db: Session):
    return db.query(models.Token).filter(
        models.Token.status == models.TokenStatus.emergency
    ).order_by(models.Token.created_at.desc()).all()

def get_dashboard_stats(db: Session):
    active = db.query(models.Token).filter(
        models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.in_progress, models.TokenStatus.emergency])
    ).count()
    
    total = db.query(models.Token).count()
    
    emergencies = db.query(models.Token).filter(
        models.Token.status == models.TokenStatus.emergency
    ).count()
    
    avg_wait = db.query(func.avg(models.Token.estimated_wait_time_mins)).filter(
        models.Token.status.in_([models.TokenStatus.waiting, models.TokenStatus.in_progress])
    ).scalar() or 0
    
    avg_rating = db.query(func.avg(models.Feedback.rating)).scalar()
    satisfaction = round((avg_rating / 4) * 5, 1) if avg_rating else 4.2
    
    return {
        "active_patients": active,
        "avg_wait_time": int(avg_wait),
        "emergency_count": emergencies,
        "satisfaction_score": satisfaction,
        "total_today": total
    }

def submit_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_token_symptoms(db: Session, token_id: int, data: dict):
    token = db.query(models.Token).filter(models.Token.id == token_id).first()
    if token:
        for key, value in data.items():
            if hasattr(token, key):
                setattr(token, key, value)
        db.commit()
        db.refresh(token)
    return token
