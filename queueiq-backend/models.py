from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum

class TokenStatus(enum.Enum):
    waiting = "waiting"
    in_progress = "in_progress"
    completed = "completed"
    emergency = "emergency"
    dropout = "dropout"

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    whatsapp_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    language = Column(String, default="en")

    tokens = relationship("Token", back_populates="patient")
    feedbacks = relationship("Feedback", back_populates="patient")

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    token_number = Column(String, unique=True, index=True)
    status = Column(Enum(TokenStatus), default=TokenStatus.waiting)
    
    # Department assignment
    department = Column(String, default="General Medicine")
    
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
