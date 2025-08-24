MedBoard AI Tutor
Overview
MedBoard AI Tutor is an intelligent, interactive chatbot designed to help medical students prepare for their board examinations. This platform provides a dynamic learning experience where students can engage with board-level clinical questions, track their performance in granular detail, and receive personalized feedback and study recommendations.

This project is architected for maximum portability and flexibility, using a containerized approach and a robust multi-provider authentication system. This allows it to be deployed on any cloud provider (GCP, Azure, AWS) or on-premise servers with minimal changes, while offering users modern, flexible sign-in options.

Features
AI-Powered Q&A: Engage in a conversational format with an AI that presents high-yield, board-style questions across all major medical disciplines.

Flexible Multi-Provider Authentication:

Standard user registration with a secure email and password.

Social sign-on with providers like Google, allowing for quick and easy access.

A foundational architecture to support institutional Single Sign-On (SSO) via SAML/OIDC for partner schools.

Secure account linking, allowing a single user to access their account via multiple login methods.

Performance Dashboard: A comprehensive analytics dashboard to visualize strengths and weaknesses. Users can filter performance by medical discipline (e.g., Biochemistry, Cardiology), anatomical region, and more.

Adaptive Learning Engine: The system intelligently suggests new questions based on past performance, focusing on areas that need improvement to ensure a robust and well-rounded knowledge base.

Unified Progress Logging: All progress, answers, and analytics are tied to a single user account, regardless of the login method used, providing a consistent and holistic view of the user's learning journey.

AI-Powered Question Categorization: Questions are automatically tagged with structured medical taxonomy including disciplines, body systems, specialties, question types, and pathophysiology mechanisms. This enables rich analytics and precise performance tracking across multiple dimensions. The system uses a cost-optimized two-step AI process with swappable LLM backends for future local model integration.

Tech Stack
Frontend: React / Next.js with Tailwind CSS.

Backend: Python with FastAPI.

Database: PostgreSQL.

ORM: SQLAlchemy for robust, type-safe interaction with the database.

Migrations: Alembic for managing database schema changes version control.

Authentication:

Core: Self-hosted JWT (JSON Web Tokens) for stateless, secure session management.

Providers: passlib for strong password hashing, Authlib for streamlined OAuth2 integration, and python3-saml for SAML/OIDC capabilities.

Testing:

Framework: Pytest for robust and scalable testing.

HTTP Client: HTTPX for asynchronous testing of API endpoints.

Mock Data: Factory Boy for generating predictable test data.

Containerization: Docker & Docker Compose for creating consistent, isolated, and portable development and deployment environments.

AI & Machine Learning: Flexible AI integration supporting both standard OpenAI and Azure OpenAI for generating high-quality questions and explanations, with automatic provider detection based on available credentials.

Getting Started (Local Development)
This project uses Docker Compose to simplify the local development setup. You can launch the entire backend stack (API server and database) with a single command.

Clone the Repository:

git clone <your-repository-url>
cd medboard-ai-tutor

Configure Environment Variables:

Create a .env file in the project root directory with the following required variables:

```bash
# Database
DATABASE_URL=sqlite:///./app.db
TEST_DATABASE_URL=sqlite:///./test.db

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# AI Service Configuration (choose one)
# Option 1: Standard OpenAI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Option 2: Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Question Tagging Backend (optional - defaults to azure_openai)
TAGGING_BACKEND=azure_openai
```

You can also copy from the example: `cp backend/.env.example .env` and modify as needed.

Launch the Backend:

From the project's root directory, run Docker Compose:

docker-compose up --build

This will build the FastAPI container, start a PostgreSQL container, and connect them. The API will be available at http://localhost:8000.

Launch the Frontend:

In a separate terminal, navigate to the frontend directory:

cd frontend

Install dependencies and start the development server:

npm install
npm run dev

The React application will be available at http://localhost:3000.

**Frontend Environment Variables (Optional):**

The frontend automatically detects the API URL based on the environment. For custom configurations, create a `.env.local` file in the `frontend/` directory:

```bash
# Frontend Environment Variables (optional)
# For local development, defaults to http://localhost:8000
# For production deployment, set to your backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production deployment (e.g., Render.com), set:
```bash
NEXT_PUBLIC_API_URL=https://your-backend-domain.onrender.com
```

## Development vs Production Commands

### Frontend (Next.js)
- **Development**: `npm run dev` - Hot reloading, development optimizations, runs on port 3000
- **Production Build**: `npm run build` - Creates optimized production build
- **Production Server**: `npm run start` - Serves the built production files

### Backend (FastAPI)
- **Development**: `uvicorn backend.main:app --reload` - Auto-reload on changes, runs on port 8000
- **Production**: `uvicorn backend.main:app --host 0.0.0.0 --port 8000` - No auto-reload, optimized for production

Testing
This project uses pytest for comprehensive testing. Tests are designed to be run against an isolated test database to ensure they are independent and do not affect development data.

Test Database: A separate test database is automatically created and torn down for the test suite.

Mock Data: factory-boy is used to create consistent and realistic mock data for users, identities, and other models, ensuring tests are predictable.

Running Tests: To run the complete test suite, navigate to the backend directory and execute pytest:

cd backend
pytest

Contributing
We welcome contributions from the community! Whether you're a developer, a medical professional, or a student, your input is valuable. Please see CONTRIBUTING.md for guidelines on how to get involved in the project.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
