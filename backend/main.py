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
        "*"  # Allow all origins for now (can restrict later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables and handle migrations
@app.on_event("startup")
async def startup_event():
    from sqlalchemy import text
    from backend.database import SessionLocal
    
    # Create all tables (safe - won't overwrite existing)
    models.Base.metadata.create_all(bind=engine)
    
    # Add missing columns if they don't exist (safe migration)
    db = SessionLocal()
    try:
        # Check and add missing columns to questions table
        missing_columns = [
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS options TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS topics TEXT", 
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS disciplines TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS body_systems TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS specialties TEXT",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS question_type VARCHAR",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS age_group VARCHAR",
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS acuity VARCHAR", 
            "ALTER TABLE questions ADD COLUMN IF NOT EXISTS pathophysiology TEXT",
            "ALTER TABLE responses ADD COLUMN IF NOT EXISTS feedback TEXT"
        ]
        
        for sql in missing_columns:
            db.execute(text(sql))
        db.commit()
        
    except Exception as e:
        print(f"Migration warning (likely safe): {e}")
        db.rollback()
    finally:
        db.close()

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
