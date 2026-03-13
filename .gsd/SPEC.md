# SPEC: QueueIQ Backend

## Status: FINALIZED

## Overview
QueueIQ Backend is a Python FastAPI service providing real-time hospital queue intelligence, voice symptom triage, and patient education. It integrates with WhatsApp (Twilio API) for patient interaction, and a React Dashboard for hospital staff.

## Core Stack
- **API Framework**: FastAPI
- **Database**: PostgreSQL (Patient records, token history)
- **Queue/Cache**: Redis (Real-time tracking, live wait times)
- **Vector DB**: ChromaDB / FAISS (Medical Knowledge base)
- **Speech/Language**: OpenAI Whisper, IndicTrans2
- **NLP/NER**: BioBERT
- **LLM**: Gemini 3.0 (Patient Education)
- **ML Models**: Gradient Boosting/LSTM for Wait prediction, Logistic Regression for Emergency Triage.

## Key Features & APIs
1. **WhatsApp Webhook (`/webhook/whatsapp`)**: Handle incoming messages, QR reads, voice notes.
2. **Queue Management API (`/api/queue`)**: Register tokens, status, real-time updates.
3. **Symptom Triage API (`/api/triage`)**: Process voice -> text (Whisper/IndicTrans2), extract symptoms (BioBERT), check emergency.
4. **Health Education API (`/api/education`)**: Generate RAG-based info using Gemini.
5. **Dashboard API (`/api/dashboard`)**: Analytics, emergency alerts, active wait times.

## Non-Functional Requirements
- **Performance**: Twilio webhooks must respond < 10s.
- **Scalability**: Redis handles concurrent real-time queue states.

## Acceptance Criteria
- End-to-end flow works: simulate WhatsApp MSG -> System predicts wait -> System extracts symptoms -> System flags emergency or standard -> Dashboard updates.
