from pydantic import BaseModel, EmailStr

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- User Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Question/Answer Schemas ---
class Question(BaseModel):
    id: int
    content: str
    discipline: str | None = None

    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    user_answer: str

# --- Analytics Schemas ---
class DisciplinePerformance(BaseModel):
    discipline: str
    total_answered: int
    correct_count: int
    accuracy: float

class AnalyticsSummary(BaseModel):
    performance_by_discipline: list[DisciplinePerformance]