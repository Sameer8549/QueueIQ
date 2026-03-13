"""
QueueIQ Personalized Health Education Engine (PRD Module 3)
Simulates: Gemini 3.0 via RAG pipeline constrained to WHO/ICMR/NHP guidelines

In production:
  - ChromaDB/FAISS vector store with WHO, ICMR, NHP documents
  - Gemini 3.0 generates personalized briefs
  - Rule-based post-processor strips drug names and dosages
  - Output in patient's detected language
"""

# Condition-matched health education briefs (RAG simulation)
HEALTH_BRIEFS = {
    "headache": {
        "title": "Understanding Your Headache",
        "condition_summary": "Headaches can have many causes including stress, dehydration, eye strain, or infections. Based on your symptoms, your doctor will determine the specific type and appropriate care.",
        "what_to_expect": [
            "The doctor may check your blood pressure and neurological responses",
            "You may be asked about recent sleep patterns and stress levels",
            "If needed, the doctor may recommend further tests"
        ],
        "questions_to_ask": [
            "How long should I expect these headaches to continue?",
            "Are there lifestyle changes that could help?",
            "Should I keep a headache diary?"
        ],
        "reminders": ["Current medications", "Recent vision changes", "Family history of migraines"]
    },
    "fever": {
        "title": "Understanding Your Fever",
        "condition_summary": "Fever is your body's natural response to fighting infection. Common causes include viral infections, bacterial infections, and inflammatory conditions. Your doctor will identify the underlying cause.",
        "what_to_expect": [
            "Temperature and vitals will be recorded",
            "Blood tests may be recommended to check infection markers",
            "The doctor will examine your throat, ears, and chest"
        ],
        "questions_to_ask": [
            "When should I be concerned about the fever returning?",
            "How much fluid should I drink daily?",
            "Should I avoid any activities while recovering?"
        ],
        "reminders": ["Duration of fever", "Any recent travel", "Contact with sick individuals"]
    },
    "cough": {
        "title": "Understanding Your Cough",
        "condition_summary": "A persistent cough may be associated with respiratory infections, allergies, or environmental factors. Your doctor will listen to your lungs and determine the best course of evaluation.",
        "what_to_expect": [
            "The doctor will use a stethoscope to listen to your breathing",
            "A throat examination will be performed",
            "A chest X-ray may be suggested if the cough has persisted"
        ],
        "questions_to_ask": [
            "Is my cough likely viral or bacterial?",
            "How long should I wait before a follow-up?",
            "Should I avoid cold food or drinks?"
        ],
        "reminders": ["Whether cough is dry or productive", "Any blood in sputum", "Smoking history"]
    },
    "joint pain": {
        "title": "Understanding Your Joint Pain",
        "condition_summary": "Joint pain can result from injury, inflammation, or wear-and-tear. The location, pattern, and severity of pain help your doctor identify the cause.",
        "what_to_expect": [
            "Physical examination of the affected joint",
            "Range of motion assessment",
            "Possible X-ray or blood tests for inflammation markers"
        ],
        "questions_to_ask": [
            "Is this related to arthritis or an acute injury?",
            "What exercises are safe for me?",
            "Should I use hot or cold compresses?"
        ],
        "reminders": ["History of injuries", "Morning stiffness duration", "Family history of arthritis"]
    },
    "stomach pain": {
        "title": "Understanding Your Stomach Pain",
        "condition_summary": "Abdominal pain has many possible causes including gastritis, infections, or dietary issues. The location and type of pain helps your doctor narrow down the cause.",
        "what_to_expect": [
            "The doctor will press on different areas of your abdomen",
            "You may be asked about your diet and bowel habits",
            "Blood tests or ultrasound may be recommended"
        ],
        "questions_to_ask": [
            "Should I follow a specific diet right now?",
            "When should I come back if pain continues?",
            "Are there foods I should avoid?"
        ],
        "reminders": ["Location of pain (upper, lower, left, right)", "Recent food consumption", "Any blood in stool"]
    },
    "chest pain": {
        "title": "⚠️ Chest Pain — Please Tell Staff Immediately",
        "condition_summary": "Chest pain requires immediate medical attention. While it may have non-serious causes like muscle strain or acidity, it must be evaluated promptly to rule out cardiac conditions.",
        "what_to_expect": [
            "An ECG (electrocardiogram) will likely be performed immediately",
            "Blood tests to check cardiac enzymes",
            "You may be placed on monitoring equipment"
        ],
        "questions_to_ask": [
            "Do my test results indicate a cardiac concern?",
            "What lifestyle changes should I make?",
            "When should I seek emergency help again?"
        ],
        "reminders": ["Exact time pain started", "Whether pain spreads to arm/jaw/back", "Diabetes or blood pressure history"]
    },
    "skin rash": {
        "title": "Understanding Your Skin Condition",
        "condition_summary": "Skin rashes can be caused by allergies, infections, or autoimmune conditions. Visual examination by the doctor is usually the first step in diagnosis.",
        "what_to_expect": [
            "The doctor will carefully examine the affected areas",
            "You may be asked about recent contact with new products",
            "Allergy testing may be suggested if needed"
        ],
        "questions_to_ask": [
            "Is this rash contagious?",
            "Should I avoid sun exposure?",
            "What moisturizers are safe to use?"
        ],
        "reminders": ["New soaps, detergents, or foods", "Allergies to medications", "Whether rash is spreading"]
    },
    "default": {
        "title": "Preparing for Your Consultation",
        "condition_summary": "Based on the symptoms you reported, our system has prepared some general guidance to help you make the most of your consultation with the doctor.",
        "what_to_expect": [
            "The doctor will take your vitals (blood pressure, temperature)",
            "A focused physical examination based on your symptoms",
            "Possible referral for tests if needed"
        ],
        "questions_to_ask": [
            "How long should my symptoms take to resolve?",
            "Are there warning signs I should watch for?",
            "When should I schedule a follow-up?"
        ],
        "reminders": ["All current medications", "Any known allergies", "Family medical history"]
    }
}


def generate_health_brief(symptoms: list, language: str = "en") -> dict:
    """
    Generate a personalized health education brief based on symptoms.
    In production, this calls Gemini 3.0 with RAG from medical knowledge base.
    """
    # Match symptoms to the best brief
    matched_key = "default"
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        for key in HEALTH_BRIEFS:
            if key in symptom_lower:
                matched_key = key
                break
        if matched_key != "default":
            break
    
    brief = HEALTH_BRIEFS[matched_key]
    
    return {
        "title": brief["title"],
        "condition_summary": brief["condition_summary"],
        "what_to_expect": brief["what_to_expect"],
        "questions_to_ask": brief["questions_to_ask"],
        "reminders": brief["reminders"],
        "language": language,
        "disclaimer": "This information is for educational purposes only and does not replace professional medical advice. Your doctor will determine the appropriate diagnosis and treatment."
    }
