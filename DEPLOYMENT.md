++++++# QueueIQ Deployment Guide

This guide explains how to deploy the full QueueIQ system to production across Railway (Backend) and Vercel (Frontend).

## 1. Backend & Database Deployment (Railway)

Railway is the official host for the QueueIQ backend and PostgreSQL database.

### Steps:
1. **GitHub Connection**: Push your code to a GitHub repository.
2. **Create Project**: On [Railway.app](https://railway.app), click **New Project** -> **Deploy from GitHub repo**.
3. **Provision Database**:
    - Once the project is created, click **"New"** -> **"Database"** -> **"Add PostgreSQL"**.
    - Railway will automatically provide a `DATABASE_URL` to your backend service.
4. **Configure Backend**:
    - Click on your backend service (repository).
    - Go to the **Variables** tab and add:
        - `GEMINI_API_KEY`: Your key from Google AI Studio.
        - `GEMINI_MODEL`: `gemini-3.1-pro-preview`
        - `PORT`: `8000`
5. **Deployment**: Railway will detect the `Dockerfile` and start the FastAPI server.

---

## 2. Frontend Deployment (Vercel)

Deploy the two frontends as separate projects for maximum speed and scale.

### App 1: Patient Mobile App (`queueiq-app`)
1. **New Project**: In [Vercel](https://vercel.com), import your GitHub repo.
2. **Root Directory**: Set this to `queueiq-app`.
3. **Build Settings**: Framework: **Other**, Build: (Empty), Output: `.`.
4. **Deploy**.

### App 2: Staff Portal (`queueiq-staff`)
1. **New Project**: In Vercel, import the same repo.
2. **Root Directory**: Set this to `queueiq-staff`.
3. **Project Name**: `queueiq-staff`.
4. **Deploy**.

---

## 3. Post-Deployment Setup (Seeding)

Once the backend is live, you need to seed the database with initial staff and patient data.
1. Connect to your Railway service via terminal.
2. Run:
   ```bash
   cd queueiq-backend
   python seed_staff.py
   python seed_patients.py
   ```

---

## 💡 Pro Tip: CORS
By default, the backend allows ALL origins (`*`). For better security, once you have your Vercel URLs, update `main.py` in the backend:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-patient-app.vercel.app", "https://your-staff-portal.vercel.app"],
    ...
)
```
