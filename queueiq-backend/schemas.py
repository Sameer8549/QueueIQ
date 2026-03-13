from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models import TokenStatus

# ─── Patient ───
class PatientBase(BaseModel):
    whatsapp_number: str
    name: Optional[str] = None
    language: str = "en"

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    class Config:
        from_attributes = True

# ─── Token ───
class TokenCreate(BaseModel):
    patient_id: int
    chief_complaint: Optional[str] = None
    department: str = "General Medicine"

class TokenResponse(BaseModel):
    id: int
    patient_id: int
    token_number: str
    status: TokenStatus
    department: str
    chief_complaint: Optional[str] = None
    symptoms_text: Optional[str] = None
    severity: str
    extracted_symptoms: Optional[str] = None
    duration: Optional[str] = None
    red_flags: Optional[str] = None
    estimated_wait_time_mins: int
    queue_position: int
    prescription_text: Optional[str] = None
    follow_up_date: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ─── Feedback ───
class FeedbackCreate(BaseModel):
    patient_id: int
    rating: int  # 0-4
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    patient_id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

# ─── Dashboard ───
class DashboardStats(BaseModel):
    active_patients: int
    avg_wait_time: int
    emergency_count: int
    satisfaction_score: float
    total_today: int

class AnalyticsData(BaseModel):
    hourly_patients: List[int]
    department_load: dict
    top_complaints: List[dict]
    language_distribution: dict
