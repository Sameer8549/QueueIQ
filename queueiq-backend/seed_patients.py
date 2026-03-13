import requests
import random
import time

API = "http://localhost:8000"

patients = [
    {"name": "Ananya Sharma", "phone": "whatsapp:+919876543210"},
    {"name": "Vikram Singh", "phone": "whatsapp:+919876500001"},
    {"name": "Priya Patel", "phone": "whatsapp:+919876500002"},
    {"name": "Rahul Verma", "phone": "whatsapp:+919876500003"},
    {"name": "Neha Gupta", "phone": "whatsapp:+919876500004"},
    {"name": "Aditya Rao", "phone": "whatsapp:+919876500005"},
    {"name": "Kavya Reddy", "phone": "whatsapp:+919876500006"},
    {"name": "Rohan Deshmukh", "phone": "whatsapp:+919876500007"},
    {"name": "Sneha Iyer", "phone": "whatsapp:+919876500008"},
    {"name": "Amit Joshi", "phone": "whatsapp:+919876500009"},
    {"name": "Ayesha Khan", "phone": "whatsapp:+919876500010"},
    {"name": "Karan Malhotra", "phone": "whatsapp:+919876500011"},
    {"name": "Pooja Hegde", "phone": "whatsapp:+919876500012"},
    {"name": "Siddharth Menon", "phone": "whatsapp:+919876500013"},
    {"name": "Riya Das", "phone": "whatsapp:+919876500014"},
]

print("Seeding demo data into QueueIQ...")

for p in patients:
    # 1. Register Patient
    print(f"Registering {p['name']}...")
    res = requests.post(f"{API}/api/queue/patient", json={"name": p['name'], "whatsapp_number": p['phone']})
    if res.status_code != 200:
        continue
    patient_id = res.json()["id"]
    
    # 2. Assign Token
    res = requests.post(f"{API}/api/queue/token", json={"patient_id": patient_id})
    if res.status_code != 200:
        continue
    token_id = res.json()["id"]
    print(f"  Assigned Token: {res.json()['token_number']}")
    
    # 3. Simulate Intake (Randomly to get different severities and symptoms)
    if random.random() > 0.2: # 80% have completed intake
        print("  Running AI simulated intake...")
        # Webhook API requires an external call for real system, but we can hit simulate-intake
        try:
            intake_res = requests.get(f"{API}/webhook/simulate-intake?token_id={token_id}")
            data = intake_res.json()
            print(f"  -> Extracted: {data['extraction'].get('chief_complaint', 'Unknown')}")
        except Exception as e:
            print(f"  Intake failed: {e}")
            
    # 4. Give some feedback for older tokens
    if random.random() > 0.6:
        requests.post(f"{API}/api/feedback/", json={"patient_id": patient_id, "rating": random.choice([3, 4, 4, 4, 5])})

    time.sleep(1)

print("Seeding complete! Dashboard should now reflect realistic data.")
