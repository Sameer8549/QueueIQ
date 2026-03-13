from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String)
    code = Column(String, unique=True, index=True) # For QR matching
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    staff = relationship("Staff", back_populates="hospital")
    tokens = relationship("Token", back_populates="hospital")

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True) # "123"
    name = Column(String)
    password_hash = Column(String)
    role = Column(String) # "doctor", "nurse", "admin"
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    
    hospital = relationship("Hospital", back_populates="staff")

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    token_number = Column(String, index=True)
    patient_name_masked = Column(String) # "P**** K****"
    age = Column(Integer)
    gender = Column(String)
    language_code = Column(String) # "kn", "hi", etc.
    phone_number = Column(String) # "+91..."
    
    department = Column(String)
    status = Column(String, default="waiting") # "waiting", "called", "consultation", "done", "emergency-routed"
    
    # AI Data
    transcription = Column(Text, nullable=True)
    clinical_summary = Column(JSON, nullable=True) # Gemini JSON
    patient_brief = Column(JSON, nullable=True) # Patient-friendly brief
    emergency_risk = Column(JSON, nullable=True) # Gemini JSON
    whatsapp_enabled = Column(Boolean, default=False)
    
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    called_at = Column(DateTime, nullable=True)
    
    hospital = relationship("Hospital", back_populates="tokens")

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Symptom data
    chief_complaint = Column(String, nullable=True)
    symptoms_text = Column(Text, nullable=True)
    severity = Column(String, default="normal")  # normal, moderate, critical
    
    # NER extracted entities
    extracted_symptoms = Column(Text, nullable=True)  # JSON string
    duration = Column(String, nullable=True)
    red_flags = Column(Text, nullable=True)  # JSON string
    
    # Wait estimates
    estimated_wait_time_mins = Column(Integer, default=0)
    queue_position = Column(Integer, default=0)
    
    # Prescription / post-visit
    prescription_text = Column(Text, nullable=True)
    follow_up_date = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    patient = relationship("Patient", back_populates="tokens")

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    rating = Column(Integer)  # 0-4  (Poor, Meh, Okay, Good, Great)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("Patient", back_populates="feedbacks")
