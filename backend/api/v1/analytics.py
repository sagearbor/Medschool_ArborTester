from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from backend import schemas
from backend.main import get_db
from backend.models import User, Response, Question
from backend.api.dependencies import get_current_user
from backend.services.test_data_service import get_demo_analytics_data

router = APIRouter()

@router.get("/summary", response_model=schemas.AnalyticsSummary)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    useTestData: bool = False
):
    """
    Returns a performance summary for the authenticated user,
    grouped by medical discipline.
    """
    if useTestData:
        return get_demo_analytics_data()

    performance_stats = db.query(
        Question.discipline,
        func.count(Response.id).label("total_answered"),
        func.sum(case((Response.is_correct == True, 1), else_=0)).label("correct_count")
    ).join(
        Question, Response.question_id == Question.id
    ).filter(
        Response.user_id == current_user.id
    ).group_by(
        Question.discipline
    ).all()

    performance_by_discipline = [
        schemas.DisciplinePerformance(
            discipline=row.discipline,
            total_answered=row.total_answered,
            correct_count=row.correct_count,
            accuracy=(row.correct_count / row.total_answered) if row.total_answered > 0 else 0
        ) for row in performance_stats
    ]

    return {"performance_by_discipline": performance_by_discipline}