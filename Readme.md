# QueueIQ

**AI-powered hospital queue intelligence platform — built for India's multilingual healthcare reality**

## Overview

QueueIQ is an intelligent queue management system designed to reduce patient wait times and confusion in hospitals, especially high-traffic government facilities. It combines a Retrieval-Augmented Generation (RAG) pipeline with medical-domain language understanding to give patients real-time, accurate guidance — in their own language.

Built during **Matrix Fusion 4.0**, where it reached the finale round.

## The Problem

Hospital queues in India are often chaotic. Patients are unsure how long they'll wait, what step comes next, or where to go — and for a large share of patients, language is an additional barrier since most hospital systems default to English or Hindi.

## Approach

QueueIQ was built around one core constraint from day one: **it has to work for everyone, regardless of language.**

- **RAG Pipeline** — Built on ChromaDB for vector storage and Gemini for response generation, enabling context-aware answers to patient queries
- **BioBERT** — Used for understanding medical terminology and context within patient queries
- **Whisper** — Enables voice input, so patients who can't easily read or type can still interact with the system
- **12 Indian Languages** — Full multilingual support, not bolted on as an afterthought but designed as the foundation
- **FastAPI Backend** — Ties the entire pipeline together into a single, fast, deployable service

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Vector Store | ChromaDB |
| LLM | Gemini |
| Medical NLP | BioBERT |
| Speech-to-Text | Whisper |
| Deployment | Vercel |

## Status

Live deployment on Vercel, with a working backend handling real queries end-to-end.

## Built By

Sameer (Abdul Sameer) — [GitHub](https://github.com/Sameer8549) · [Portfolio](https://asameer.netlify.app) · [LinkedIn](https://linkedin.com/in/abdulsameer9)

---

*Built with Team Cipher for Matrix Fusion 4.0*