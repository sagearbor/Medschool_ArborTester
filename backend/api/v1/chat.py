from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import logging

from backend import schemas
from backend.database import get_db
from backend.models import User, Question, Response
from backend.api.dependencies import get_current_user
from backend.services.openai_service import OpenAIService

logger = logging.getLogger(__name__)
openai_service = OpenAIService()

router = APIRouter()

@router.get("/question", response_model=schemas.Question)
def get_next_question(
    specialty: str = "General Medicine",
    difficulty: str = "Intermediate", 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Generate a new clinical question using Azure OpenAI or return existing question.
    """
    try:
        # Generate new question using OpenAI
        question_data = openai_service.generate_clinical_question(
            specialty=specialty,
            difficulty=difficulty
        )
        
        # Store in database
        question = Question(
            content=question_data["question"],
            discipline=question_data["specialty"],
            options=json.dumps(question_data["options"]),
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
            difficulty=question_data["difficulty"],
            topics=json.dumps(question_data.get("topics", []))
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        # Log question generation for analytics
        logger.info(f"Generated question {question.id} for user {current_user.id} - Specialty: {specialty}, Difficulty: {difficulty}")
        
        return question
        
    except Exception as e:
        logger.error(f"Error generating question: {str(e)}")
        # Fallback to existing question or placeholder
        question = db.query(Question).first()
        if not question:
            question = Question(
                content="Sample clinical question: A 45-year-old patient presents with chest pain. What is the most appropriate next step?",
                discipline=specialty,
                options='{"A": "ECG", "B": "Chest X-ray", "C": "Blood work", "D": "Discharge home"}',
                correct_answer="A",
                explanation="ECG is the most appropriate first step for chest pain evaluation."
            )
            db.add(question)
            db.commit()
            db.refresh(question)
        return question

@router.post("/answer")
def submit_answer(
    answer_in: schemas.AnswerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit and evaluate user's answer to a question with AI feedback.
    """
    question = db.query(Question).filter(Question.id == answer_in.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer is correct
    is_answer_correct = answer_in.user_answer.upper() == question.correct_answer.upper()
    
    # Generate personalized feedback using AI
    feedback_data = openai_service.evaluate_answer(
        question=question.content,
        correct_answer=question.correct_answer,
        user_answer=answer_in.user_answer,
        explanation=question.explanation or ""
    )

    # Store response in database
    response = Response(
        user_id=current_user.id,
        question_id=answer_in.question_id,
        user_answer=answer_in.user_answer,
        is_correct=is_answer_correct,
        feedback=feedback_data.get("feedback", "")
    )
    db.add(response)
    db.commit()
    
    # Log answer submission for analytics
    logger.info(f"User {current_user.id} answered question {question.id} - Correct: {is_answer_correct}")

    return {
        "status": "Answer submitted",
        "is_correct": is_answer_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "personalized_feedback": feedback_data.get("feedback", ""),
        "question_id": question.id
    }