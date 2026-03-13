from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, security
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

class LoginRequest(BaseModel):
    employee_id: str
    password: str

class ForgotPasswordRequest(BaseModel):
    employee_id: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.employee_id == request.employee_id).first()
    if not staff:
        raise HTTPException(status_code=401, detail="Invalid employee ID")
    
    if not security.verify_password(request.password, staff.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")
    
    access_token = security.create_access_token(
        data={"sub": staff.employee_id, "role": staff.role, "name": staff.name}
    )
    
    # Get hospital name
    hospital = db.query(models.Hospital).filter(models.Hospital.id == staff.hospital_id).first()
    hospital_name = hospital.name if hospital else "QueueIQ Hospital"
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "staff_name": staff.name,
        "hospital_name": hospital_name,
        "role": staff.role
    }

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Simulation: In a real app, this would send an email.
    staff = db.query(models.Staff).filter(models.Staff.employee_id == request.employee_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Employee ID not found")
    
    return {"message": "Reset link sent to your registered email."}

@router.post("/sso")
def sso_login():
    # Placeholder for Hospital SSO
    return {"message": "Redirecting to Hospital SSO provider..."}
