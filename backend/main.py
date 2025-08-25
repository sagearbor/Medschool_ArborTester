from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

from backend.api.v1 import auth as auth_router
from backend.api.v1 import chat as chat_router
from backend.api.v1 import analytics as analytics_router
from backend.database import engine
from backend import models

# Load environment variables
load_dotenv()

app = FastAPI(title="MedBoard AI Tutor")

# Add Session middleware for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("JWT_SECRET_KEY", "fallback-secret-key"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        "https://*.onrender.com"  # Allow all Render.com subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=engine)

# --- API Routers ---
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat_router.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(analytics_router.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}
