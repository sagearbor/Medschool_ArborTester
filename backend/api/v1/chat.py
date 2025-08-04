from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import schemas
from backend.main import get_db
from backend.models import User, Question, Response
from backend.api.dependencies import get_current_user

router = APIRouter()

@router.get("/question", response_model=schemas.Question)
def get_next_question(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    This endpoint provides the next question for the user.
    """
    # Placeholder implementation:
    question = db.query(Question).first()
    if not question:
        question = Question(content="This is a placeholder question from the database.", discipline="General")
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
    This endpoint receives the user's answer to a question.
    """
    question = db.query(Question).filter(Question.id == answer_in.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_answer_correct = True # Placeholder

    response = Response(
        user_id=current_user.id,
        question_id=answer_in.question_id,
        user_answer=answer_in.user_answer,
        is_correct=is_answer_correct
    )
    db.add(response)
    db.commit()

    return {"status": "Answer submitted", "is_correct": is_answer_correct}