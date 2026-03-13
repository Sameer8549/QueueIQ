from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QueueIQ API", version="2.0.0", description="AI-Powered Hospital Queue Intelligence")

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from routers import auth, queue, whatsapp, dashboard, feedback, symptoms
app.include_router(auth.router)
app.include_router(queue.router)
app.include_router(whatsapp.router)
app.include_router(dashboard.router)
app.include_router(feedback.router)
app.include_router(symptoms.router)
from routers import emergency
app.include_router(emergency.router)

# ─── WebSocket for real-time queue updates (PRD Module 1) ───
connected_clients: list[WebSocket] = []

@app.websocket("/ws/queue")
async def queue_websocket(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Keep connection alive, receive any messages
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_queue_update(data: dict):
    """Broadcast queue state changes to all connected clients"""
    for client in connected_clients:
        try:
            await client.send_json(data)
        except:
            connected_clients.remove(client)

@app.get("/")
def root():
    return {
        "app": "QueueIQ",
        "version": "2.0.0",
        "modules": [
            "Queue Prediction Engine",
            "Voice Symptom Pre-Assessment",
            "Health Education Engine",
            "Emergency Triage Re-Router",
            "Operations Intelligence Dashboard",
            "Post-Visit Tracker"
        ]
    }
