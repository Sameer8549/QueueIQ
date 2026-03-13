from database import SessionLocal, engine
import models, security

models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()
    
    # Add Hospital
    hospital = db.query(models.Hospital).filter(models.Hospital.code == "QH001").first()
    if not hospital:
        hospital = models.Hospital(
            name="Wenlock District Hospital",
            location="Mangaluru, Karnataka",
            code="QH001"
        )
        db.add(hospital)
        db.flush()
    
    # Add Staff (Employee 123 / Password 2525)
    staff = db.query(models.Staff).filter(models.Staff.employee_id == "123").first()
    if not staff:
        staff = models.Staff(
            employee_id="123",
            name="Dr. Priya Sharma",
            password_hash=security.get_password_hash("2525"),
            role="doctor",
            hospital_id=hospital.id
        )
        db.add(staff)
    
    db.commit()
    db.close()
    print("Database seeded successfully with Hospital and Staff 123.")

if __name__ == "__main__":
    seed()
