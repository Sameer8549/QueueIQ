"""
QueueIQ Emergency Triage Re-Router (PRD Module 4)
Simulates: Logistic Regression Classifier + Rule-Based Layer

In production:
  - Logistic Regression trained on labeled emergency datasets
  - Rule-based override for absolute red-flag keywords
  - System errs on caution — false positives acceptable
"""

# Expanded red-flag keyword library
RED_FLAG_KEYWORDS = [
    # Cardiac
    "chest pain", "heart attack", "cardiac arrest", "palpitations",
    "arm radiation", "left arm pain", "crushing chest",
    # Respiratory
    "difficulty breathing", "can't breathe", "shortness of breath",
    "choking", "severe asthma", "respiratory distress", "orthopnea",
    # Neurological
    "stroke", "sudden numbness", "face drooping", "slurred speech",
    "loss of consciousness", "seizure", "convulsion", "severe headache sudden onset",
    # Hemorrhage
    "heavy bleeding", "blood in vomit", "blood in stool",
    "uncontrolled bleeding", "hemorrhage",
    # Allergic
    "anaphylaxis", "severe allergic reaction", "throat swelling",
    "tongue swelling", "difficulty swallowing",
    # Trauma
    "head injury", "unconscious", "severe burn", "fracture open wound",
    # Other critical
    "high fever unresponsive", "poisoning", "overdose",
    "diabetic emergency", "severe dehydration",
]

# Severity scores for confidence output
SEVERITY_WEIGHTS = {
    "chest pain": 0.95,
    "difficulty breathing": 0.90,
    "stroke": 0.98,
    "loss of consciousness": 0.97,
    "heavy bleeding": 0.92,
    "anaphylaxis": 0.96,
    "seizure": 0.88,
    "head injury": 0.85,
}


def check_emergency(symptom_text: str) -> dict:
    """
    Two-layer triage:
      Layer 1: Rule-based keyword matching
      Layer 2: Confidence scoring
    
    Returns: { is_emergency, confidence, detected_flags, recommended_action }
    """
    text_lower = symptom_text.lower()
    detected_flags = []
    max_confidence = 0.0
    
    for keyword in RED_FLAG_KEYWORDS:
        if keyword in text_lower:
            detected_flags.append(keyword)
            weight = SEVERITY_WEIGHTS.get(keyword, 0.75)
            max_confidence = max(max_confidence, weight)
    
    is_emergency = len(detected_flags) > 0
    
    if is_emergency:
        if max_confidence >= 0.90:
            action = "IMMEDIATE: Route to Emergency Department. Alert ER staff via WhatsApp. Patient should NOT wait in general queue."
        elif max_confidence >= 0.75:
            action = "URGENT: Flag for priority triage. Nurse assessment within 5 minutes."
        else:
            action = "ELEVATED: Move to front of queue. Monitor vitals."
    else:
        action = "STANDARD: Continue in regular queue."
    
    return {
        "is_emergency": is_emergency,
        "confidence": round(max_confidence, 2),
        "detected_flags": detected_flags,
        "recommended_action": action
    }
