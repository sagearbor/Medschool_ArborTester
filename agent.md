# agent.md — Medschool_ArborTester (MedBoard AI Tutor)

## Overview
AI-powered medical board exam prep chatbot. Presents board-style clinical questions, tracks performance, provides personalized feedback. Containerized, multi-provider auth (Google OAuth + email), deployable on any cloud.

## Tech Stack
- Python (FastAPI backend)
- React/TypeScript (frontend)
- Docker / docker-compose
- Alembic (DB migrations)
- Google OAuth
- Render (deployment)

## Status (last commits)
- Production deployment fixes (missing DB columns, migrations)
- Google OAuth redirect flow fixed
- CORS temporarily opened to all origins
- Database configuration and deployment setup done
- **Not fully stable** — recent commits are all production fixes

## How to Run
```bash
docker-compose up
# or see RENDER_DEPLOYMENT.md for cloud deploy
```

## Open Tasks
- Lock down CORS (currently `*`)
- Verify all DB migrations stable in production
- See `development_checklist.yaml`

## Branch
- Main: `main`
- Sophie working branch: `sophieArborBot_firstBranch`

## Test Strategy
- Backend: pytest (check `backend/` for test files)
- Manual: login flow (email + Google), Q&A session, score tracking
- Verify DB migrations don't break on fresh deploy
