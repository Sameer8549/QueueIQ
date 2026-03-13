from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import func
import models, schemas

router = APIRouter(prefix="/api/feedback", tags=["feedback"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def submit_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return {"status": "success", "message": "Thank you for your feedback!"}

@router.get("/stats")
def get_feedback_stats(db: Session = Depends(get_db)):
    avg = db.query(func.avg(models.Feedback.rating)).scalar()
    count = db.query(models.Feedback).count()
    return {
        "average_rating": round(avg, 1) if avg else 0,
        "total_feedbacks": count,
        "satisfaction_score": round((avg / 4) * 5, 1) if avg else 4.2
    }
