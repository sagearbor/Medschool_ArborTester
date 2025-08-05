from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import logging

from backend import schemas
from backend.database import get_db
from backend.models import User, Question, Response
from backend.api.dependencies import get_current_user
from backend.services.openai_service import OpenAIService
from backend.services.tagging_service import get_tagging_service

logger = logging.getLogger(__name__)
openai_service = OpenAIService()

router = APIRouter()

@router.get("/test")
def test_endpoint(current_user: User = Depends(get_current_user)):
    """Test endpoint to verify auth and basic functionality"""
    return {"message": "Chat API is working", "user_id": current_user.id}

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
        # Try to generate new question using OpenAI first
        logger.info(f"Attempting to generate question for specialty: {specialty}, difficulty: {difficulty}")
        question_data = openai_service.generate_clinical_question(
            specialty=specialty,
            difficulty=difficulty
        )
        logger.info(f"Successfully generated question: {question_data.get('question', 'N/A')[:100]}...")
        
        # Tag the question using AI
        try:
            tagging_service = get_tagging_service()
            tags = tagging_service.tag_question(
                question_content=question_data["question"],
                question_options=question_data["options"]
            )
            logger.info(f"Question tagged successfully: {tags}")
        except Exception as tag_error:
            logger.error(f"Error tagging question: {str(tag_error)}")
            tags = {}

        # Store in database with structured tags
        question = Question(
            content=question_data["question"],
            discipline=question_data["specialty"],  # Legacy field
            options=json.dumps(question_data["options"]),
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
            difficulty=question_data["difficulty"],
            topics=json.dumps(question_data.get("topics", [])),  # Legacy field
            
            # New structured taxonomy fields
            disciplines=json.dumps(tags.get("disciplines", [])),
            body_systems=json.dumps(tags.get("body_systems", [])),
            specialties=json.dumps(tags.get("specialties", [])),
            question_type=tags.get("question_type"),
            age_group=tags.get("age_group"),
            acuity=tags.get("acuity"),
            pathophysiology=json.dumps(tags.get("pathophysiology", []))
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        
        # Log question generation for analytics
        logger.info(f"Generated question {question.id} for user {current_user.id} - Specialty: {specialty}, Difficulty: {difficulty}")
        
        return question
        
    except Exception as e:
        logger.error(f"Error generating question with OpenAI: {str(e)}")
        
        # Fallback to existing question first
        existing_question = db.query(Question).filter(Question.discipline == specialty).first()
        if existing_question:
            logger.info(f"Returning existing question {existing_question.id} for user {current_user.id}")
            return existing_question
        
        # If no existing question, create a fallback
        try:
            fallback_content = f"Sample {specialty} clinical question: A patient presents with symptoms related to {specialty.lower()}. What is the most appropriate next diagnostic step?"
            fallback_options = {"A": "Order basic lab work", "B": "Perform physical examination", "C": "Order imaging study", "D": "Refer to specialist"}
            
            # Tag the fallback question
            try:
                tagging_service = get_tagging_service()
                fallback_tags = tagging_service.tag_question(
                    question_content=fallback_content,
                    question_options=fallback_options
                )
            except Exception:
                fallback_tags = {}
            
            fallback_question = Question(
                content=fallback_content,
                discipline=specialty,  # Legacy field
                options=json.dumps(fallback_options),
                correct_answer="B",
                explanation="A thorough physical examination is always an appropriate initial step in patient evaluation.",
                difficulty=difficulty,
                topics='["Clinical Assessment", "Diagnostic Approach"]',  # Legacy field
                
                # New structured taxonomy fields
                disciplines=json.dumps(fallback_tags.get("disciplines", [specialty.lower().replace(" ", "_")])),
                body_systems=json.dumps(fallback_tags.get("body_systems", ["general"])),
                specialties=json.dumps(fallback_tags.get("specialties", ["internal_medicine"])),
                question_type=fallback_tags.get("question_type", "diagnosis"),
                age_group=fallback_tags.get("age_group", "adult"),
                acuity=fallback_tags.get("acuity", "routine"),
                pathophysiology=json.dumps(fallback_tags.get("pathophysiology", []))
            )
            db.add(fallback_question)
            db.commit()
            db.refresh(fallback_question)
            
            logger.info(f"Created fallback question {fallback_question.id} for user {current_user.id}")
            return fallback_question
            
        except Exception as db_error:
            logger.error(f"Database error creating fallback question: {str(db_error)}")
            raise HTTPException(status_code=500, detail="Unable to generate or retrieve question")

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