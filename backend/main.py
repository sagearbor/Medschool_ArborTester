import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from backend.api.v1 import auth as auth_router
from backend.api.v1 import chat as chat_router
from backend.api.v1 import analytics as analytics_router

load_dotenv()

# --- Production Database Connection ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(title="MedBoard AI Tutor")

# --- API Routers ---
app.include_router(auth_router.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat_router.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(analytics_router.router, prefix="/api/v1/analytics", tags=["Analytics"])

# --- Dependency ---
def get_db():
    """
    FastAPI dependency to create and yield a database session for each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ok"}