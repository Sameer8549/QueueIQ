from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TokenCreate(BaseModel):
    hospital_id: int
    patient_name_masked: str
    language_code: str
    department: Optional[str] = "General OPD"
    phone_number: Optional[str] = None

class FeedbackCreate(BaseModel):
    token_id: int
    rating: int
    comment: Optional[str] = None

class PatientBrief(BaseModel):
    title: str
    condition_summary: str
    what_to_expect: List[str]
    questions_to_ask: List[str]
    reminders: List[str]

class TokenResponse(BaseModel):
    id: int
    token_number: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardOverview(BaseModel):
    patients_today: int
    avg_wait_min: int
    emergency_count: int
    satisfaction_score: float
    hospital_name: str
    doctor_on_duty: str
