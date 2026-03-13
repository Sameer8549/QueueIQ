

**PRODUCT REQUIREMENTS DOCUMENT**
**QueueIQ**
*AI-Powered Hospital Queue Intelligence & Patient Education Platform*

| | |
|---|---|
| Document Version | v1.0 — Initial Release |
| Date | March 2026 |
| Prepared For | Matrix Fusion 4.0 — Yen Artificia, YIT Moodbidri |
| Domain | Healthcare + Education (AI & ML) |
| Status | DRAFT — Hackathon Submission |

*"Turn every wasted hospital wait into informed, prepared, empowered care."*

---

**1. Executive Summary**

QueueIQ is an AI-powered hospital queue intelligence and patient education platform designed specifically for Indian government hospitals. It operates entirely through WhatsApp and a QR code — requiring zero app downloads, zero hardware investment, and zero change in hospital infrastructure.

Every day, over 10 crore patients visit government hospitals across India and wait 4 to 5 hours with no information about their turn. QueueIQ solves this with six integrated AI capabilities: real-time queue wait prediction, multilingual voice symptom intake, personalized health education while waiting, emergency triage detection, hospital operations intelligence, and post-visit medication reminders.

The result is a measurable reduction in patient wait frustration, a 40% improvement in doctor consultation efficiency, and a system that can save lives by detecting emergency-level symptoms before they are ignored in a general queue.

**One-Line Pitch:** QueueIQ puts an AI doctor's assistant in every government hospital in India — no new hardware, no app download, just a QR code and WhatsApp — predicting your wait, understanding your symptoms, educating you while you wait, and saving your life if it is an emergency.

**1.1 Key Metrics at a Glance**

| Metric | Current State | With QueueIQ |
|---|---|---|
| Average OPD wait time | 4.5 hours | Trackable — patients leave and return |
| Patient dropout rate | ~40% leave without being seen | Reduced by estimated 60% |
| Doctor consultation efficiency | 60% time on basic explanation | 40% time saved per consultation |
| Emergency detection in OPD | Zero — patients wait silently | Real-time AI triage alert |
| Hardware required | Token dispensers — expensive | Zero — one printed QR code |

---

**2. Problem Statement**

**2.1 The Scale of the Problem**

India's government hospital system handles over 10 crore outpatient visits every day across 25,778 government hospitals. Despite this massive scale, the patient experience in OPD queues remains completely unintelligent — a problem that affects the poorest and most vulnerable populations who have no alternative.

**2.2 Core Problem Areas**

**Problem 1 — Zero Queue Intelligence**
Token display screens in government hospitals show a number. Nothing more. No prediction of wait time. No communication with the patient. No notification when their turn is approaching. Patients are forced to sit in crowded waiting rooms for 4 to 5 hours staring at a number board, unable to leave for food, medicine, or to attend to family.

**Problem 2 — Massive Patient Dropout**
Approximately 40% of patients in government hospital OPDs leave without being seen. Not because they recovered — but because they could not afford to wait. A daily wage worker who loses a day's income waiting for a doctor is making a healthcare sacrifice with permanent consequences. Children miss diagnoses. Chronic conditions go undetected. Emergencies escalate.

**Problem 3 — Wasted Consultation Time**
The average government hospital doctor sees 60 to 80 patients per day. In each consultation, an estimated 60% of time is spent asking basic questions the patient could have answered before entering the room — what is your problem, how long, which medications, any allergies. This is time stolen from actual diagnosis and treatment.

**Problem 4 — Invisible Emergencies in General Queues**
Emergency patients do not always arrive at the emergency entrance. A patient describing chest pain, stroke symptoms, or severe allergic reaction often enters through the general OPD and takes a token number. No system currently detects these high-risk signals and re-routes patients to emergency care. Every year, people die in OPD queues because this gap exists.

**Problem 5 — Zero Patient Preparation**
Patients arrive at government hospitals with no understanding of what to expect, what to mention, or what their condition might mean. This is not a failure of intelligence — it is a failure of access to health information in the patient's own language. Most existing health education content is in English, requires literacy, and assumes smartphone and internet proficiency that the majority of government hospital patients do not have.

**Problem Summary:** The problem is not a lack of doctors or hospitals. India has both. The problem is zero intelligence in the system that connects patients to care — no prediction, no communication, no education, no triage. QueueIQ is the intelligence layer the system is missing.

---

**3. Product Overview**

**3.1 What QueueIQ Is**

QueueIQ is a WhatsApp-native, AI-powered platform that works as an intelligent layer on top of any existing hospital queue system. A patient scans a QR code at the hospital entrance, registers their token number through WhatsApp, speaks their symptoms in their regional language, and immediately enters an AI-driven flow that predicts their wait time, educates them about their condition, monitors for emergencies, and alerts them before their turn.

Hospital staff access a real-time web dashboard that shows live queue status, AI-generated patient symptom summaries, emergency alerts, and predictive analytics for rush-hour planning and resource allocation.

**3.2 What QueueIQ Is NOT**
- NOT a diagnostic tool — it never diagnoses conditions or recommends specific treatments
- NOT a telemedicine platform — it prepares patients for in-person visits, it does not replace them
- NOT a prescription platform — it never suggests drug names or dosages
- NOT replacing doctors — it makes every moment doctors spend more productive
- NOT an app — it works entirely through WhatsApp which patients already use

**3.3 Target Users**

| User Type | Description | Primary Need |
|---|---|---|
| OPD Patients | Government hospital outpatients — primarily low-income, multilingual, varying literacy | Know when their turn is. Understand their condition. Not waste a full day. |
| Hospital Doctors | OPD physicians seeing 60–80 patients per day | See patient history and symptoms before patient enters room. Consult faster. |
| Hospital Staff / Admin | Reception, queue managers, administrators, CMOs | Reduce crowd pressure. Get rush-hour predictions. Handle emergencies proactively. |
| District Health Officers | Government officials overseeing multiple hospitals | Aggregate analytics. ABDM compliance. Performance reporting. |

---

**4. Product Goals & Success Metrics**

**4.1 Primary Goals**
- Reduce effective patient wait frustration by giving real-time queue position and wait time prediction with greater than 85% accuracy
- Improve doctor consultation efficiency by delivering structured symptom summaries before every patient consultation
- Prevent emergency deaths in OPD by detecting critical symptom flags and alerting emergency staff within 60 seconds
- Educate patients in their native language about their condition, what to expect, and what to communicate to the doctor
- Provide hospital administrators with predictive intelligence for staffing, scheduling, and capacity planning

**4.2 Success Metrics**

| Metric | Target (3 months) | Target (12 months) |
|---|---|---|
| Wait time prediction accuracy | ±15 minutes | ±8 minutes |
| Patient dropout rate reduction | 20% improvement | 60% improvement |
| Doctor time saved per consultation | 2 minutes per patient | 4 minutes per patient |
| Emergency detection recall | Greater than 90% | Greater than 97% |
| Patient satisfaction score | 3.5 / 5 | 4.3 / 5 |
| Hospitals onboarded | 3 pilot hospitals | 50 hospitals |

---

**5. Features & AI Modules**

**5.1 AI Module 1 — Intelligent Queue Prediction Engine**
Predict each patient's wait time accurately and update it in real time as the queue moves. Uses Gradient Boosting for baseline prediction and LSTM (Keras) for real-time refinement. Learns hospital-specific patterns, accounts for patient complexity, and detects anomalies. Patient receives WhatsApp notification 15 minutes before their predicted turn.

**5.2 AI Module 2 — Voice Symptom Pre-Assessment**
Patient sends a WhatsApp voice note in any of 12 Indian languages. OpenAI Whisper transcribes it, IndicTrans2 translates to English, fine-tuned BioBERT performs NER extracting chief complaint, duration, severity, associated symptoms, and red flags. Structured summary pushed to doctor's dashboard before patient enters.

Supported languages: Hindi, Kannada, Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi, Odia, Assamese, Urdu.

**5.3 AI Module 3 — Personalized Health Education Engine**
Gemini 3.0 via RAG pipeline constrained to WHO guidelines, ICMR protocols, and NHP India content generates a personalized education brief. Delivered as WhatsApp text and optional voice note in the patient's language. A rule-based post-processor removes all drug names, dosages, and treatment recommendations before delivery. All language uses terms like 'may suggest', 'commonly associated with', 'your doctor will determine'.

**5.4 AI Module 4 — Emergency Triage Re-Router**
A logistic regression classifier plus rule-based layer screens every symptom summary in real time. On detection, immediate alert sent to emergency desk WhatsApp and displayed on staff dashboard as critical alert with pulsing red indicator. Patient receives WhatsApp message to go to Emergency immediately. Token flagged as emergency-routed. System errs on caution — false positives far less harmful than missing a real emergency.

**5.5 AI Module 5 — Hospital Operations Intelligence Dashboard**
7-day rush hour forecast, doctor efficiency tracking, department overload alerts, patient language distribution, top complaint trends, and anomaly detection. Anomaly detection flags unusual patterns — sudden spike in fever cases may indicate local outbreak requiring public health response.

**5.6 AI Module 6 — Post-Visit Medication & Follow-Up Tracker**
Doctor enters prescription via dashboard or photo via Tesseract + PaddleOCR. Daily WhatsApp reminders for each medicine at the correct time in the patient's language. Follow-up appointment reminder 24 hours before scheduled date. 'How are you feeling?' check-in sent 3 days post-visit. If patient reports worsening, system generates gentle alert suggesting return visit.

---

**6. Technical Architecture**

| Layer | Technology | Purpose |
|---|---|---|
| Patient Interface | WhatsApp Business API (Twilio) | QR scan, token registration, symptom input, alerts |
| Staff Dashboard | React.js + Chart.js | Live queue management, patient summaries, emergency alerts |
| API Backend | Python FastAPI | Core business logic, AI orchestration, WhatsApp webhook |
| Queue State | Redis | Real-time queue position tracking, live wait time updates |
| Primary Database | PostgreSQL | Patient records, token history, prescription data |
| Vector Store | ChromaDB / FAISS | Medical knowledge base for RAG pipeline |
| Speech Recognition | OpenAI Whisper | Multilingual voice note transcription |
| Translation | IndicTrans2 (AI4Bharat) | Regional language to English translation |
| Symptom NER | Fine-tuned BioBERT | Extract complaints, duration, severity, red flags |
| LLM / Education | Gemini 3.0 API | Health education brief generation via RAG |
| Queue Prediction | Gradient Boosting + LSTM (Keras) | Historical pattern learning + real-time prediction |
| Emergency Detection | Logistic Regression + Rule Engine | Two-layer triage with low false-negative rate |
| OCR | Tesseract + PaddleOCR | Prescription digitization |
| Deployment | Docker + Railway / Render | Containerized, zero infrastructure cost for pilot |

**6.2 Patient Journey Flow**
1. Patient arrives and scans QR code — WhatsApp opens automatically in detected regional language
2. Patient types or speaks token number — system registers them in the queue
3. Queue Prediction Engine calculates estimated wait time and sends it to patient
4. Patient prompted to send voice note describing symptoms
5. Whisper transcribes — IndicTrans2 translates if needed
6. Emergency Triage module screens symptom text — red flag detected triggers immediate alert
7. BioBERT NER extracts structured symptom data — pushed to doctor dashboard
8. Gemini 3.0 generates personalized health education brief in patient's language
9. Wait time updates continuously — patient receives 15-minute advance alert
10. Post-visit: prescription digitized, daily medication reminders begin, 3-day follow-up check-in sent

---

**7. Feasibility Analysis**

**7.1 Technical Feasibility**
Every component is built on mature, open-source technology. OpenAI Whisper supports all target languages with accuracy above 90%. IndicTrans2 is best-in-class for Indian language translation. BioBERT has pre-trained medical NER models on HuggingFace. Gemini 3.0 API accessible via Google AI Studio. Twilio WhatsApp sandbox activates within minutes. A functional prototype can be built in 20 to 24 hours by a team of 3 to 4 developers.

**7.2 Operational Feasibility**
Zero hardware required — hospitals need only one printed QR code per entry point. Zero training required for patients. Minimal staff training — dashboard designed for non-technical reception staff. No changes to existing hospital systems. Pilot deployment possible within one week of completing MVP.

**7.3 24-Hour Hackathon Build Plan**

| Hours | Module | Deliverable |
|---|---|---|
| 0–3 | Queue ML | Simulate queue data, train wait-time model, live prediction on dashboard |
| 3–8 | WhatsApp Flow | Twilio integration, QR entry, token registration, live wait time to patient |
| 8–14 | Voice Intake | Whisper transcription, BioBERT extraction, structured summary on dashboard |
| 14–18 | Education AI | Gemini 3.0 generating health brief in Kannada and Hindi |
| 18–21 | Emergency | Triage classifier wired to dashboard red alert, chest pain detection demo |
| 21–24 | Demo Polish | End-to-end demo polished, presentation finalized, walkthrough rehearsed |

---

**8. Novelty & Competitive Landscape**

| Feature | QueueIQ | Qmatic/TokenMax | Practo/Apollo | iCall/Wysa | Govt Portals |
|---|---|---|---|---|---|
| AI Wait Prediction | ✅ | No | No | No | No |
| Voice Symptom Intake | ✅ | No | No | No | No |
| 12 Indian Languages | ✅ | No | Partial | No | Partial |
| Patient Education (AI) | ✅ | No | Generic | Generic | No |
| Emergency Triage | ✅ | No | No | No | No |
| Zero App Download | ✅ | No | No | No | Yes |
| Zero Hardware | ✅ | No | Yes | Yes | Yes |
| Govt Hospital Ready | ✅ | Partial | No | No | Yes |
| Free for Hospitals | ✅ (pilot) | No | No | No | Yes |

---

**9. Commercial Viability**

**Primary — B2G:** License to state/district health authorities under ABDM framework. Pricing: Rs. 2,000–5,000 per hospital per month. At 1% adoption of 25,778 government hospitals = Rs. 5–13 crore annual recurring revenue.

**Secondary — B2B:** White-label API to private hospital chains, telemedicine platforms, health insurance companies. Pricing: Rs. 2–5 per patient interaction.

**Tertiary — NGO/CSR:** Free deployment in rural PHCs funded through Tata Trusts, Azim Premji Foundation, WHO India, USAID.

**Market Size:** Indian health technology market projected at Rs. 8,000 crore by 2027 (27% CAGR). Target addressable market: Rs. 1,500 crore annually. ABDM digitization budget: Rs. 1,600 crore over 5 years.

| Challenge | Risk | Mitigation |
|---|---|---|
| Hospital admin resistance | High | Free 2-week pilot, zero effort. Use ABDM mandate as entry point. |
| LLM generating inaccurate content | High | RAG constrained to WHO/ICMR/NHP. Rule-based filter removes all drug/dosage content. |
| Poor rural internet | Medium | Functional on 2G. Top 50 complaint briefs cached locally. |
| Dialect variation / ASR errors | Medium | IndicTrans2 trained on dialect variants. Fallback to text symptom form. |
| Patient privacy | Medium | Voice notes deleted within 60 seconds. Token number only — no PII required. |

---

**10. References**

1. Radford, A. et al. Robust Speech Recognition via Large-Scale Weak Supervision. OpenAI Whisper. ICML 2023.
2. AI4Bharat. IndicTrans2. arXiv:2305.16307, 2023.
3. Lee, J. et al. BioBERT. Bioinformatics, 2020. arXiv:1901.08746
4. Meta AI Research. The LLaMA 3 Herd of Models. arXiv:2407.21783, 2024.
5. Lewis, P. et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020.
6. National Health Portal India — OPD Queue and Hospital Statistics 2023-24. nhp.gov.in
7. National Rural Health Mission Annual Report 2023-24. mohfw.gov.in
8. Ayushman Bharat Digital Mission (ABDM). abdm.gov.in

---

