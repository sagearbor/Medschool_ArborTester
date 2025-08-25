# Render.com Deployment Guide

## 1. Database Setup on Render

**Create PostgreSQL Database:**
- Go to Render.com dashboard
- Click "New" → "PostgreSQL"
- Database name: `medboard-db`
- User: `medboard_user` (auto-generated)
- Copy the **Internal Database URL** (starts with `postgresql://`)
     - postgresql://medboard_db_user:MZWTAlShLzaor6n1zNBuwDAlcLXTomIo@dpg-d2kkt03ipnbc73f7pmi0-a/medboard_db

## 2. Backend Service Environment Variables

Set these in Render.com backend service dashboard:

```bash
# Database (use Internal Database URL from step 1)
DATABASE_URL=postgresql://medboard_user:password@internal-host:5432/medboard_db

# JWT
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Azure OpenAI (add your actual credentials)
AZURE_OPENAI_API_KEY=your_azure_openai_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Question Tagging Backend
TAGGING_BACKEND=azure_openai

# Google OAuth (optional - add if you set up Google Console)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 3. Build Command for Render Backend

```bash
pip install -r requirements.txt
```

## 4. Start Command for Render Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## 5. Database Migration

Render will auto-run migrations on startup via the `startup_event()` in `main.py`:
```python
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=engine)
```

## 6. Frontend Environment Variable

Update your frontend's `NEXT_PUBLIC_API_URL`:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-service.onrender.com
```

## 7. CORS Update (if needed)

The backend already allows all origins (`"*"`), so it should work with your deployed frontend.

---

**Ready to deploy after local testing!**
