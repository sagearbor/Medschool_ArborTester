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

    # Get all user responses with their question details
    user_responses = db.query(Response, Question).join(
        Question, Response.question_id == Question.id
    ).filter(
        Response.user_id == current_user.id
    ).all()

    # Parse structured disciplines from each question and aggregate
    discipline_stats = {}
    
    for response, question in user_responses:
        # Parse disciplines from JSON field (fallback to legacy field)
        try:
            import json
            disciplines = json.loads(question.disciplines) if question.disciplines else [question.discipline or "General Medicine"]
        except:
            disciplines = [question.discipline or "General Medicine"]
        
        # Count stats for each discipline this question belongs to
        for discipline in disciplines:
            if discipline not in discipline_stats:
                discipline_stats[discipline] = {"total": 0, "correct": 0}
            
            discipline_stats[discipline]["total"] += 1
            if response.is_correct:
                discipline_stats[discipline]["correct"] += 1

    performance_by_discipline = [
        schemas.DisciplinePerformance(
            discipline=discipline,
            total_answered=stats["total"],
            correct_count=stats["correct"],
            accuracy=(stats["correct"] / stats["total"]) if stats["total"] > 0 else 0
        ) for discipline, stats in discipline_stats.items()
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