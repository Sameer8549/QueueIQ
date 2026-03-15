import sys
import os
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models

def seed_demo_data():
    db = SessionLocal()
    try:
        # Wipe existing demo data (Optional: only wipe non-critical tables)
        db.query(models.Analytics).delete()
        db.query(models.Feedback).delete()
        db.query(models.Token).delete()
        db.commit()

        print("Creating fresh demo patients...")
        
        # 1. Critical Scenario
        t1 = models.Token(
            token_number="TK-1001",
            hospital_id=1,
            patient_name_masked="A**** K****",
            department="Emergency / Cardiology",
            status="waiting",
            wait_min=5,
            language_code="en",
            transcription="I have severe pain in my chest and my left arm is going numb.",
            clinical_summary="Patient reports acute chest pain radiating to left arm. High risk of myocardial infarction. Immediate triage required.",
            clinical_assessment_json='{"urgency": "critical", "condition": "Possible MI"}'
        )
        db.add(t1)

        # 2. Pediatric Fever
        t2 = models.Token(
            token_number="TK-1002",
            hospital_id=1,
            patient_name_masked="Child of R.S.",
            department="Pediatrics",
            status="waiting",
            wait_min=25,
            language_code="hi",
            transcription="My baby has high fever and is crying non-stop for 4 hours.",
            clinical_summary="Pediatric patient with high fever (reported) and persistent crying. Needs assessment for infection or dehydration.",
        )
        db.add(t2)

        # 3. Regular Checkup
        t3 = models.Token(
            token_number="TK-1003",
            hospital_id=1,
            patient_name_masked="M**** L****",
            department="General Medicine",
            status="consultation",
            wait_min=0,
            language_code="en",
            transcription="Regular blood pressure checkup appointment.",
            clinical_summary="Routine follow-up for hypertension management.",
        )
        db.add(t3)

        db.commit()
        print("Demo Seeded Successfully! 🚀")

    except Exception as e:
        print(f"Error seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_data()
