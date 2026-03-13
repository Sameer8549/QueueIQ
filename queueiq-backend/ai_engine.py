"""
QueueIQ AI Engine — Voice Symptom Pre-Assessment (PRD Module 2)
Simulates: OpenAI Whisper transcription + IndicTrans2 translation + BioBERT NER

In production this calls:
  1. Whisper API for multilingual speech-to-text
  2. IndicTrans2 for regional language → English
  3. Fine-tuned BioBERT for Named Entity Recognition
"""
import random
import json

# Simulated symptom scenarios (like realistic hospital visits)
SCENARIOS = [
    {
        "transcription": "I have been having persistent headaches for the past 3 days, along with mild fever and body pain. I also feel dizzy when I stand up quickly.",
        "chief_complaint": "Persistent Headache",
        "symptoms": ["headache", "fever", "body pain", "dizziness"],
        "duration": "3 days",
        "severity": "moderate",
        "red_flags": [],
        "department": "General Medicine"
    },
    {
        "transcription": "My child has been coughing continuously for a week. She has runny nose and is not eating properly. Temperature is around 100 degrees.",
        "chief_complaint": "Persistent Cough in Child",
        "symptoms": ["cough", "runny nose", "loss of appetite", "low-grade fever"],
        "duration": "1 week",
        "severity": "moderate",
        "red_flags": [],
        "department": "Pediatrics"
    },
    {
        "transcription": "I slipped and fell on my knee two days ago. It is very swollen and I cannot bend it properly. The pain is getting worse.",
        "chief_complaint": "Knee Injury",
        "symptoms": ["knee swelling", "limited mobility", "increasing pain"],
        "duration": "2 days",
        "severity": "moderate",
        "red_flags": [],
        "department": "Orthopedics"
    },
    {
        "transcription": "I am experiencing severe chest pain that radiates to my left arm. I am also feeling very short of breath and nauseous.",
        "chief_complaint": "Chest Pain with Radiation",
        "symptoms": ["chest pain", "left arm pain", "shortness of breath", "nausea"],
        "duration": "acute onset",
        "severity": "critical",
        "red_flags": ["chest pain", "arm radiation", "shortness of breath"],
        "department": "Emergency"
    },
    {
        "transcription": "I have had a skin rash on my arms and legs for the last 5 days. It is itchy and spreading. I have not taken any new medicines.",
        "chief_complaint": "Spreading Skin Rash",
        "symptoms": ["skin rash", "itching", "progressive spread"],
        "duration": "5 days",
        "severity": "normal",
        "red_flags": [],
        "department": "Dermatology"
    },
    {
        "transcription": "My stomach has been hurting badly since morning. I vomited twice and have loose motions. I also feel very weak.",
        "chief_complaint": "Acute Gastroenteritis",
        "symptoms": ["abdominal pain", "vomiting", "diarrhea", "weakness"],
        "duration": "since morning",
        "severity": "moderate",
        "red_flags": [],
        "department": "General Medicine"
    },
    {
        "transcription": "I have difficulty breathing especially when lying down. My ankles are swollen and I feel very tired climbing stairs.",
        "chief_complaint": "Dyspnea with Edema",
        "symptoms": ["dyspnea", "orthopnea", "ankle edema", "exercise intolerance"],
        "duration": "1 week",
        "severity": "critical",
        "red_flags": ["difficulty breathing", "orthopnea", "edema"],
        "department": "Cardiology"
    },
    {
        "transcription": "I have ear pain since yesterday night. I cannot hear properly from my right ear. There is some discharge also.",
        "chief_complaint": "Ear Pain with Discharge",
        "symptoms": ["ear pain", "hearing loss", "ear discharge"],
        "duration": "1 day",
        "severity": "normal",
        "red_flags": [],
        "department": "ENT"
    }
]


def transcribe_audio(media_url: str) -> str:
    """Simulate Whisper transcription of a voice note"""
    scenario = random.choice(SCENARIOS)
    return scenario["transcription"]


def extract_symptoms(text: str) -> dict:
    """Simulate BioBERT NER extraction from transcribed text"""
    # Try to match the transcription back to a scenario
    matched = None
    for s in SCENARIOS:
        if s["transcription"] == text:
            matched = s
            break
    
    if not matched:
        matched = random.choice(SCENARIOS)
    
    return {
        "chief_complaint": matched["chief_complaint"],
        "symptoms": matched["symptoms"],
        "duration": matched["duration"],
        "severity": matched["severity"],
        "red_flags": matched["red_flags"],
        "department": matched["department"],
        "extracted_symptoms_json": json.dumps(matched["symptoms"]),
        "red_flags_json": json.dumps(matched["red_flags"])
    }
