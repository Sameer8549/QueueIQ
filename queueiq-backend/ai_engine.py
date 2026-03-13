import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Optional local AI models (heavy)
try:
    import whisper
    whisper_model = whisper.load_model("base")
except Exception as e:
    print(f"Whisper warning: {e}")
    whisper_model = None

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    # IndicTrans2 setup would happen here
    # tokenizer = AutoTokenizer.from_pretrained("ai4bharat/indictrans2-en-indic-1b", trust_remote_code=True)
    # it2_model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/indictrans2-en-indic-1b", trust_remote_code=True)
except Exception as e:
    print(f"Transformers warning: {e}")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
try:
    from twilio.rest import Client
except Exception as e:
    print(f"Twilio warning: {e}")

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
else:
    model = None

twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except:
        pass

class AIEngine:
    @staticmethod
    async def generate_clinical_summary(token_number, age, gender, transcription, conditions):
        if not model:
            return {"dashboard_headline": "AI Engine Offline", "severity": "moderate"}
            
        system_prompt = """
        You are QueueIQ's Clinical Pre-Assessment Engine for Indian government hospitals. 
        Generate a structured clinical summary a doctor can read in 10 seconds. 
        Output strict JSON only:
        {
          "summary": {
            "dashboard_headline": "<15 words max>",
            "chief_complaint": "<1 sentence>",
            "severity": "mild" | "moderate" | "severe",
            "red_flags": ["<flag1>", "<flag2>"],
            "suggested_vitals": ["<vital1>", "<vital2>"],
            "emergency_score": <0-100>,
            "patient_complexity": "standard" | "complex" | "emergency"
          },
          "patient_brief": {
            "title": "Possible <Condition>",
            "condition_summary": "<Reassuring 2-sentence summary>",
            "what_to_expect": ["<Step 1>", "<Step 2>", "<Step 3>"],
            "questions_to_ask": ["<Q1>", "<Q2>", "<Q3>"],
            "reminders": ["<Reminder 1>", "<Reminder 2>"]
          }
        }
        NEVER include drug names or treatment recommendations.
        """
        # RAG: Retrieve relevant SOP context
        from vector_engine import vector_engine
        sop_context = vector_engine.query(transcription)
        
        user_prompt = f"Patient token: {token_number}. Age: {age}. Gender: {gender}. Transcribed complaint: '{transcription}'. Known conditions: {conditions}. \nRelevant Hospital SOP Context: {sop_context}\nGenerate dual JSON for doctor and patient."
        
        try:
            response = model.generate_content(system_prompt + "\n\n" + user_prompt)
            data = json.loads(response.text.strip().replace('```json', '').replace('```', ''))
            return data
        except Exception as e:
            print(f"Gemini Error: {e}")
            return {"dashboard_headline": "Summary unavailable", "severity": "moderate"}

    @staticmethod
    async def get_emergency_triage(token, age, transcription, conditions, vitals=None):
        if not model: return {"is_emergency": False}
        
        system_prompt = """
        You are QueueIQ's Emergency Triage Engine for Indian government hospitals. 
        Assess patient symptoms for emergency risk. BIAS: when uncertain classify as emergency.
        Output strict JSON:
        {
          "is_emergency": true | false,
          "emergency_category": "CARDIAC"|"NEUROLOGICAL"|"RESPIRATORY"|"TRAUMA"|"PEDIATRIC"|"ANAPHYLAXIS"|"HEMORRHAGE"|"DIABETIC"|"OTHER"|"NONE",
          "triage_score": <0-100>,
          "confidence": "high"|"medium"|"low",
          "alert_message_for_staff": "<30 words max — clinical specific>",
          "patient_whatsapp_message": "<warm urgent message>",
          "recommended_action": "<1 sentence>"
        }
        """
        # RAG: Retrieve relevant SOP context
        from vector_engine import vector_engine
        sop_context = vector_engine.query(transcription)

        user_prompt = f"Token: {token}. Age: {age}. Transcription: '{transcription}'. Known conditions: {conditions}. Vitals: {vitals}. \nRelevant Hospital SOP Context: {sop_context}\nGenerate emergency triage JSON."
        
        try:
            response = model.generate_content(system_prompt + "\n\n" + user_prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', ''))
        except:
            return {"is_emergency": False}

    @staticmethod
    async def get_operational_insights(hospital_name, patient_count, avg_wait, peak_hour, busiest_dept):
        if not model: return {"insight": "Operations stable."}
        
        system_prompt = """
        You are QueueIQ's Hospital Operations Intelligence Engine.
        Analyze today's queue data and generate a 2-sentence insight for the hospital administrator.
        Output strict JSON: { "insight": "<2 sentences>", "recommendation": "<1 action item>" }
        """
        user_prompt = f"Hospital: {hospital_name}. Patients today: {patient_count}. Avg wait: {avg_wait} min. Peak hour: {peak_hour}. Busiest dept: {busiest_dept}. Generate insight JSON."
        
        try:
            response = model.generate_content(system_prompt + "\n\n" + user_prompt)
            return json.loads(response.text.strip().replace('```json', '').replace('```', ''))
    @staticmethod
    async def transcribe_and_translate(audio_path: str, language_code: str = "en"):
        # 1. ASR using Whisper
        if whisper_model:
            result = whisper_model.transcribe(audio_path)
            transcription = result["text"]
        else:
            transcription = "Simulated: Patient reports acute abdominal pain since morning."

        # 2. Translation using IndicTrans2 (Simulated fallback)
        # If language is not English, use Gemini as a high-quality translator + reasoning engine
        if language_code != "en" and model:
            translate_prompt = f"Translate the following medical complaint from {language_code} to English: '{transcription}'"
            try:
                translated = model.generate_content(translate_prompt)
                return translated.text.strip(), transcription
            except:
                pass
        
        return transcription, transcription # (English, Original)

    @staticmethod
    async def send_whatsapp_message(to_number: str, message: str):
        if not twilio_client:
            print(f"Twilio Offline. Would send to {to_number}: {message}")
            return False
            
        try:
            # Ensure number is in E.164 format and prefixed with whatsapp:
            formatted_to = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
            
            twilio_client.messages.create(
                from_=TWILIO_WHATSAPP_NUMBER,
                body=message,
                to=formatted_to
            )
            return True
        except Exception as e:
            print(f"Twilio Error: {e}")
            return False
