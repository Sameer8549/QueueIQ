from database import SessionLocal
import models
import datetime

def seed_patients():
    db = SessionLocal()
    hospital = db.query(models.Hospital).filter(models.Hospital.code == "QH001").first()
    if not hospital:
        print("Run seed_staff.py first.")
        return

    patients = [
        {
            "token": "A-101",
            "name": "Ramesh Kumar",
            "age": 45,
            "gender": "Male",
            "lang": "kn",
            "dept": "General Medicine",
            "transcription": "I have been having severe stomach pain and nausea for the past 2 days.",
            "summary": {
                "dashboard_headline": "Abdominal pain with nausea (2 days)",
                "severity": "moderate",
                "emergency_score": 35
            }
        },
        {
            "token": "B-202",
            "name": "Sunita Devi",
            "age": 32,
            "gender": "Female",
            "lang": "hi",
            "dept": "Pediatrics",
            "transcription": "My child has high fever since morning and is not eating anything.",
            "summary": {
                "dashboard_headline": "Pediatric high fever, poor intake",
                "severity": "severe",
                "emergency_score": 65
            }
        },
        {
            "token": "C-303",
            "name": "Anjali S.",
            "age": 28,
            "gender": "Female",
            "lang": "ta",
            "dept": "OPD",
            "transcription": "I have a sharp headache and blurred vision starting an hour ago.",
            "summary": {
                "dashboard_headline": "Acute headache with vision changes",
                "severity": "severe",
                "emergency_score": 85
            }
        }
    ]

    for p in patients:
        existing = db.query(models.Token).filter(models.Token.token_number == p["token"]).first()
        if not existing:
            token = models.Token(
                token_number=p["token"],
                patient_name_masked=p["name"][0] + "**** " + p["name"].split()[-1][0] + "****",
                age=p["age"],
                gender=p["gender"],
                language_code=p["lang"],
                department=p["dept"],
                transcription=p["transcription"],
                clinical_summary=p["summary"],
                patient_brief={
                    "title": "Health Update",
                    "condition_summary": "Your assessment is being reviewed by the medical team.",
                    "what_to_expect": ["Check-in at desk", "Vitals check", "Doctor consultation"],
                    "questions_to_ask": ["How long will recovery take?", "Are there lifestyle changes needed?"],
                    "reminders": ["Stay hydrated", "Keep your token handy"]
                },
                hospital_id=hospital.id,
                status="waiting" if p["summary"]["severity"] != "severe" else "called"
            )
            db.add(token)
    
    db.commit()
    db.close()
    print("Seeded patients successfully.")

if __name__ == "__main__":
    seed_patients()
