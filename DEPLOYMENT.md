++++++# QueueIQ Deployment Guide

This guide explains how to deploy the full QueueIQ system to production across Railway (Backend) and Vercel (Frontend).

## 1. Backend Deployment (Railway)

The backend is built with FastAPI and is ready for Railway using the root-level `Dockerfile`.

### Steps:
1. **GitHub Connection**: Push your code to a GitHub repository.
2. **Create Project**: On Railway, click **New Project** -> **Deploy from GitHub repo**.
3. **Environment Variables**: Add the following in the **Variables** tab:
    - `GEMINI_API_KEY`: Your Google AI Studio key.
    - `GEMINI_MODEL`: `gemini-3.1-pro-preview`
    - `TWILIO_ACCOUNT_SID`: (Optional) For WhatsApp.
    - `TWILIO_AUTH_TOKEN`: (Optional) For WhatsApp.
    - `TWILIO_WHATSAPP_NUMBER`: (Optional) `whatsapp:+14155238886`.
    - `DATABASE_URL`: Railway will provide this if you add a PostgreSQL plugin.
4. **PostgreSQL**: 
    - Click **New** -> **Database** -> **Add PostgreSQL**.
    - Railway will automatically inject the `DATABASE_URL`.
5. **Deployment**: Railway will detect the `Dockerfile` and deploy at a URL like `https://queueiq-backend-production.up.railway.app`.

---

## 2. Frontend Deployment (Vercel)

Since there are two frontend apps (`queueiq-app` and `queueiq-staff`), you should deploy them as two separate Vercel projects.

### App 1: Patient Mobile App (`queueiq-app`)
1. **New Project**: In Vercel, import your GitHub repo.
2. **Root Directory**: Set this to `queueiq-app`.
3. **Build Settings**: 
    - Framework Preset: **Other**
    - Build Command: (Leave empty)
    - Output Directory: `.`
4. **API URL Update**: 
    - Once your Railway backend is live, open `queueiq-app/index.html` (and other pages).
    - Update the `API_URL` variable in the `<script>` tag to your Railway URL.

### App 2: Staff Portal (`queueiq-staff`)
1. **New Project**: In Vercel, import your GitHub repo.
2. **Root Directory**: Set this to `queueiq-staff`.
3. **Build Settings**: Same as above.
4. **API URL Update**: Update the `API_URL` variable in `Main_Dashboard.html`, etc.

---

## 3. Alternative: All-in-One Deployment (Render)

Since you have a `render.yaml` file, you can deploy everything to Render in one go.

### Steps:
1. **GitHub Connection**: Push code to GitHub.
2. **Create Project**: On Render, go to **Blueprints** -> **New Blueprint Instance**.
3. **Select Repo**: Connect your QueueIQ repo.
4. **Environment Variables**: Render will ask for variables for each service (Backend, App, Staff).
    - Ensure `GEMINI_API_KEY` is set for the backend.
5. **Database**: Render will automatically create the PostgreSQL instance defined in the blueprint (if applicable) or you can add one manually.

---

## 4. Alternate Zero-Cost Options (No Credit Card)

If you'd like to avoid trial limits:

### 1. Database & Backend: Render (Free Tier)
- **Why**: Render offers a free PostgreSQL tier (limited to 30 days) and free web service hosting. 
- **Steps**:
  - Sign up at [Render.com](https://render.com/).
  - Follow the **Section 3** instructions for Blueprint deployment.
  - It is essentially "zero cost" for the first 30 days of development/testing.

### 2. Backend: Hugging Face Spaces (Docker)
- **Why**: Always-on FastAPI hosting, free.
- **Note**: You will need a database URL. If not using a cloud DB, the backend will reset its data on every restart.

### 3. Frontends: Vercel
- **Why**: Industry standard for static sites, always free.

---

## 5. Post-Deployment Setup (Seeding)

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
