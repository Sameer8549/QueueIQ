from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TokenCreate(BaseModel):
    token_number: str
    hospital_id: int
    language_code: str

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
