import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    print("1. Creating Patient...")
    patient_res = requests.post(f"{BASE_URL}/api/queue/patient", json={
        "whatsapp_number": "whatsapp:+919876543210",
        "name": "Test User"
    })
    print(patient_res.json())
    patient_id = patient_res.json()["id"]

    print("\n2. Generating Token...")
    token_res = requests.post(f"{BASE_URL}/api/queue/token", json={
        "patient_id": patient_id
    })
    print(token_res.json())

    print("\n3. Sending WhatsApp Audio Note (Webhook)...")
    webhook_res = requests.post(
        f"{BASE_URL}/webhook/whatsapp", 
        data={
            "From": "whatsapp:+919876543210",
            "Body": "",
            "MediaUrl0": "http://example.com/audio.ogg"
        }
    )
    print(webhook_res.json())

    print("\n4. Checking Active Queue...")
    queue_res = requests.get(f"{BASE_URL}/api/queue/active")
    print(json.dumps(queue_res.json(), indent=2))

if __name__ == "__main__":
    test_flow()
