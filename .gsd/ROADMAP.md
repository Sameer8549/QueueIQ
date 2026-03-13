# QueueIQ Backend Roadmap

## Phase 1: Foundation (FastAPI & DB)
- Set up FastAPI project structure (`queueiq-backend`).
- Configure PostgreSQL database & SQLAlchemy models (Patients, Tokens).
- Set up Redis connection for Queue State.

## Phase 2: Webhook & Basic Queue
- Implement Twilio WhatsApp Webhook endpoint.
- Build logic to register a patient token and calculate baseline wait time.
- API for Dashboard to view live queue.

## Phase 3: AI Modules (Mocked/Integrated)
- Integrate Whisper/IndicTrans2 for audio processing.
- Integrate BioBERT for NER (Symptom extraction).
- Implement Emergency Triage rules engine.
- Integrate Gemini 3.0 for Health Education RAG.

## Phase 4: Integration
- Connect all flows so that WhatsApp interaction triggers AI processing and updates Dashboard API in real-time.
