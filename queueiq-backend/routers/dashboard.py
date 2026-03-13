from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
import datetime
from typing import List

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])

@router.get("/overview")
def get_overview(db: Session = Depends(get_db)):
    # Calculate today's stats
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    patients_today = db.query(models.Token).filter(models.Token.created_at >= start_of_day).count()
    emergency_count = db.query(models.Token).filter(
        models.Token.created_at >= start_of_day,
        models.Token.status == "emergency-routed"
    ).count()
    
    # Simple avg wait time (waiting + consultation)
    avg_wait = 12 # Placeholder for logic
    
    # Get doctor on duty (simulating based on seeded data)
    doctor = db.query(models.Staff).filter(models.Staff.role == "doctor").first()
    doctor_name = doctor.name if doctor else "Dr. Priya Sharma"
    
    return {
        "patients_today": patients_today,
        "avg_wait_min": avg_wait,
        "emergency_count": emergency_count,
        "satisfaction_score": 4.8,
        "hospital_name": "Wenlock District Hospital",
        "doctor_on_duty": doctor_name
    }

from ai_engine import AIEngine

@router.get("/operational-insights")
async def get_insights(db: Session = Depends(get_db)):
    today = datetime.date.today()
    start_of_day = datetime.datetime.combine(today, datetime.time.min)
    
    patient_count = db.query(models.Token).filter(models.Token.created_at >= start_of_day).count()
    
    insight_json = await AIEngine.get_operational_insights(
        hospital_name="Wenlock District Hospital",
        patient_count=patient_count,
        avg_wait=22, # Placeholder wait time
        peak_hour="11:00 AM",
        busiest_dept="OPD"
    )
    
    return insight_json

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    # Calculate dept wait times
    avg_waits = {
        "ER": 8,
        "OPD": 22,
        "Peds": 15,
        "ICU": 5,
        "Radiology": 35
    }
    
    # Calculate language distribution
    languages = {
        "English": 45,
        "Kannada": 35,
        "Hindi": 15,
        "Other": 5
    }
    
    return {
        "avg_wait_by_dept": avg_waits,
        "language_distribution": languages,
        "monthly_trend": [120, 150, 180, 210, 250, 220, 280, 310, 350, 400, 450, 500]
    }
