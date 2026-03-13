from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import random

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    return crud.get_dashboard_stats(db)

@router.get("/emergencies")
def get_emergencies(db: Session = Depends(get_db)):
    tokens = crud.get_emergency_tokens(db)
    return [{
        "id": t.id,
        "token_number": t.token_number,
        "patient_id": t.patient_id,
        "chief_complaint": t.chief_complaint or "Unspecified Emergency",
        "symptoms_text": t.symptoms_text,
        "severity": t.severity,
        "department": t.department,
        "estimated_wait_time_mins": t.estimated_wait_time_mins,
        "red_flags": t.red_flags,
        "created_at": str(t.created_at)
    } for t in tokens]

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    """Simulated analytics data for the Operations Intelligence Dashboard (PRD Module 5)"""
    return {
        "hourly_patients": [random.randint(5, 15) for _ in range(12)],
        "department_load": {
            "General Medicine": random.randint(30, 60),
            "Pediatrics": random.randint(10, 30),
            "Orthopedics": random.randint(8, 20),
            "ENT": random.randint(5, 15),
            "Dermatology": random.randint(5, 12),
            "Cardiology": random.randint(8, 18),
            "Gynecology": random.randint(10, 25),
        },
        "top_complaints": [
            {"complaint": "Fever & Cold", "count": random.randint(20, 45)},
            {"complaint": "Headache", "count": random.randint(15, 35)},
            {"complaint": "Joint Pain", "count": random.randint(10, 25)},
            {"complaint": "Cough", "count": random.randint(12, 28)},
            {"complaint": "Stomach Pain", "count": random.randint(8, 20)},
        ],
        "language_distribution": {
            "Hindi": random.randint(35, 50),
            "Kannada": random.randint(20, 35),
            "English": random.randint(10, 20),
            "Tamil": random.randint(5, 15),
            "Telugu": random.randint(3, 10),
        },
        "rush_hours": [
            {"hour": "09:00", "predicted": random.randint(20, 50)},
            {"hour": "10:00", "predicted": random.randint(30, 55)},
            {"hour": "11:00", "predicted": random.randint(40, 60)},
            {"hour": "12:00", "predicted": random.randint(25, 45)},
            {"hour": "14:00", "predicted": random.randint(30, 50)},
            {"hour": "15:00", "predicted": random.randint(25, 40)},
            {"hour": "16:00", "predicted": random.randint(15, 30)},
        ],
        "anomalies": [
            {
                "type": "Spike Detected",
                "detail": f"Fever cases up {random.randint(30,60)}% in last 2 hours — possible local outbreak",
                "severity": "warning"
            }
        ]
    }
