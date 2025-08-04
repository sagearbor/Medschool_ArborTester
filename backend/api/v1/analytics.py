from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from backend import schemas
from backend.database import get_db
from backend.models import User, Response, Question
from backend.api.dependencies import get_current_user
from backend.services.test_data_service import get_demo_analytics_data
from backend.services.analytics_service import analytics_service

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

@router.get("/detailed")
def get_detailed_analytics(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive user performance analytics with logging data.
    """
    return analytics_service.get_user_performance_stats(current_user.id, db, days)

@router.get("/system-stats")
def get_system_statistics(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get system-wide usage statistics (admin/monitoring endpoint).
    """
    return analytics_service.get_system_usage_stats(db, days)