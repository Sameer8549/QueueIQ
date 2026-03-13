from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
import time
import random

def create_hospital(db: Session, name: str, location: str, code: str):
    db_hospital = models.Hospital(name=name, location=location, code=code)
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital

def create_token(db: Session, req: schemas.TokenCreate):
    # Simple token generation logic
    prefix = req.department[:1].upper() if req.department else "P"
    count = db.query(models.Token).count() + 1
    token_val = f"{prefix}-{100 + count}"
    
    db_token = models.Token(
        token_number=token_val,
        patient_name_masked=req.patient_name_masked,
        language_code=req.language_code,
        department=req.department,
        hospital_id=req.hospital_id,
        phone_number=req.phone_number,
        status="waiting"
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_active_tokens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Token).filter(
        models.Token.status.in_(["waiting", "called", "consultation", "emergency-routed"])
    ).order_by(models.Token.created_at.desc()).offset(skip).limit(limit).all()

def get_emergency_tokens(db: Session):
    return db.query(models.Token).filter(
        models.Token.status == "emergency-routed"
    ).order_by(models.Token.created_at.desc()).all()

def get_dashboard_stats(db: Session):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    patients_today = db.query(models.Token).filter(models.Token.created_at >= start_of_day).count()
    emergency_count = db.query(models.Token).filter(
        models.Token.created_at >= start_of_day,
        models.Token.status == "emergency-routed"
    ).count()
    
    avg_rating = db.query(func.avg(models.Feedback.rating)).scalar()
    satisfaction = round((avg_rating / 4) * 5, 1) if avg_rating else 4.8
    
    return {
        "active_patients": patients_today,
        "avg_wait_time": 15, # Placeholder
        "emergency_count": emergency_count,
        "satisfaction_score": satisfaction,
        "total_today": patients_today
    }

def update_token_symptoms(db: Session, token_id: int, data: dict):
    token = db.query(models.Token).filter(models.Token.id == token_id).first()
    if token:
        for key, value in data.items():
            if hasattr(token, key):
                setattr(token, key, value)
        db.commit()
        db.refresh(token)
    return token

import datetime
