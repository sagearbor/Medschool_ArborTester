# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MedBoard AI Tutor is a containerized medical education platform that helps students prepare for board exams through AI-powered Q&A, performance analytics, and adaptive learning. The system supports multi-provider authentication (email/password, OAuth, SSO) with unified progress tracking.

## Development Commands

### Backend (FastAPI)
```bash
# Start development environment with Docker
docker-compose up --build

# Start development server directly (without Docker)
# IMPORTANT: Run from project root, not from backend directory
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
cd backend
pytest

# Database migrations
cd backend
alembic upgrade head
alembic revision --autogenerate -m "description"

# Access API documentation
# http://localhost:8000/docs (Swagger UI)
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev        # Development server (http://localhost:3000)
npm run build      # Production build
npm run lint       # ESLint
```

## Architecture

### Backend Structure
- **FastAPI** application with versioned API routes (`/api/v1/`)
- **SQLAlchemy** ORM with Alembic migrations
- **PostgreSQL** database via Docker Compose
- **JWT-based** authentication with multi-provider support
- **Modular design**: separate modules for auth, chat, analytics
- **AI-Powered Question Tagging**: Automatic categorization with swappable LLM backends

### Key Models
- `User`: Core user entity with relationships to identities and responses
- `Identity`: Multi-provider authentication (email, OAuth, SAML/OIDC)
- `Question`/`Response`: Q&A system with performance tracking
- `SSOConfiguration`: Institutional SSO settings
- `UserMemory`: Condensed chat history for context

### Authentication Flow
- JWT tokens for stateless session management
- `get_current_user` dependency for protected routes
- Multi-provider identity linking to single user accounts
- Support for Google OAuth and institutional SSO

### Frontend Architecture
- **Next.js** with React components
- **Tailwind CSS** for styling
- **Axios** with JWT interceptors for API calls
- Token-based authentication with localStorage
- Component structure: pages -> components pattern

### Database
- PostgreSQL with connection pooling
- Alembic for schema versioning
- Test database isolation for pytest
- Foreign key relationships for data integrity

### Question Tagging System
- **Two-step AI process**: Question generation + structured categorization
- **Swappable backends**: Azure OpenAI (default) or local LLM via `TAGGING_BACKEND` env var
- **Structured taxonomy**: 12 orthogonal dimensions including:
  - Disciplines (anatomy, pharmacology, etc.)
  - Body systems (cardiovascular, respiratory, etc.)
  - Specialties (internal medicine, surgery, etc.)
  - Question types (diagnosis, treatment, mechanism, etc.)
  - Patient demographics (age groups, acuity levels)
  - Pathophysiology mechanisms (infectious, autoimmune, etc.)
- **Analytics-ready**: Enables rich dashboard filtering and performance tracking
- **Cost-optimized**: Designed for expensive generation model + cheap local tagging model

## Testing Strategy

### Backend Testing
- **pytest** with async support (pytest-asyncio)
- **HTTPX** client for API testing
- **Factory Boy** for mock data generation
- Test database fixtures in `conftest.py`
- Separate test DB to avoid development data contamination

### Key Test Patterns
- Authenticated client fixtures for protected endpoints
- Mock external API calls (Gemini API)
- Database transaction rollback for test isolation

## Environment Setup

### Required Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- JWT secret keys for token generation
- OAuth provider credentials (Google, etc.)
- Azure OpenAI credentials for question generation and tagging:
  - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
  - `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint URL
  - `AZURE_OPENAI_API_VERSION`: API version (e.g., "2024-02-01")
  - `AZURE_OPENAI_DEPLOYMENT_NAME`: Model deployment name (e.g., "gpt-4")
- Optional: `TAGGING_BACKEND`: "azure_openai" (default) or "local_llm" for question categorization

### Docker Configuration
- `docker-compose.yml` includes PostgreSQL and backend services
- Backend auto-reloads on code changes via volume mounting
- Separate Dockerfile for production builds

## Development Workflow

1. Backend changes: Test with `pytest`, apply migrations with `alembic`
2. Frontend changes: Use `npm run dev` for hot reloading
3. API changes: Update both backend routes and frontend API calls
4. Database changes: Generate migrations, test with fresh DB

## API Structure

- `/api/v1/auth/*`: Authentication endpoints (signup, login, OAuth callbacks)
- `/api/v1/chat/*`: Q&A interaction (question generation, answer submission)
- `/api/v1/analytics/*`: Performance dashboard data
- JWT-protected routes use `get_current_user` dependency

## Key Dependencies

### Backend
- FastAPI, SQLAlchemy, Alembic, psycopg2-binary
- passlib, python-jose, authlib, python3-saml
- pytest, httpx, factory-boy (testing)

### Frontend
- Next.js, React, Tailwind CSS
- axios, recharts (for analytics visualization)