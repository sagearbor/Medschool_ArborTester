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

def _extract_categories_from_question(question: Question, group_by: str) -> list:
    """Extract categories from a question based on the grouping dimension"""
    import json
    
    try:
        if group_by == "disciplines":
            if question.disciplines and question.disciplines.strip():
                parsed = json.loads(question.disciplines)
                return parsed if parsed else [question.discipline or "General Medicine"]
            return [question.discipline or "General Medicine"]
            
        elif group_by == "body_systems":
            if question.body_systems and question.body_systems.strip():
                parsed = json.loads(question.body_systems)
                return parsed if parsed else ["General"]
            return ["General"]
            
        elif group_by == "specialties":
            if question.specialties and question.specialties.strip():
                parsed = json.loads(question.specialties)
                return parsed if parsed else ["General Medicine"]
            return ["General Medicine"]
            
        elif group_by == "pathophysiology":
            if question.pathophysiology and question.pathophysiology.strip():
                parsed = json.loads(question.pathophysiology)
                return parsed if parsed else ["Unknown"]
            return ["Unknown"]
            
        elif group_by == "question_type":
            return [question.question_type] if question.question_type else ["Unknown"]
            
        elif group_by == "age_group":
            return [question.age_group] if question.age_group else ["Unknown"]
            
        elif group_by == "acuity":
            return [question.acuity] if question.acuity else ["Unknown"]
            
        else:
            # Default to disciplines
            if question.disciplines and question.disciplines.strip():
                parsed = json.loads(question.disciplines)
                return parsed if parsed else [question.discipline or "General Medicine"]
            return [question.discipline or "General Medicine"]
            
    except Exception as e:
        # Fallback on any JSON parsing error
        print(f"Error parsing categories for group_by={group_by}: {e}")
        return [question.discipline or "General Medicine"]

@router.get("/summary", response_model=schemas.AnalyticsSummary)
def get_analytics_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    useTestData: bool = False,
    group_by: str = "disciplines"
):
    """
    Returns a performance summary for the authenticated user,
    grouped by specified taxonomy dimension.
    """
    if useTestData:
        return get_demo_analytics_data(group_by)

    # Get all user responses with their question details
    user_responses = db.query(Response, Question).join(
        Question, Response.question_id == Question.id
    ).filter(
        Response.user_id == current_user.id
    ).all()

    # Aggregate stats by the selected grouping dimension
    category_stats = {}
    
    for response, question in user_responses:
        categories = _extract_categories_from_question(question, group_by)
        
        # Count stats for each category this question belongs to
        for category in categories:
            if category not in category_stats:
                category_stats[category] = {"total": 0, "correct": 0}
            
            category_stats[category]["total"] += 1
            if response.is_correct:
                category_stats[category]["correct"] += 1

    performance_by_discipline = [
        schemas.DisciplinePerformance(
            discipline=category,
            total_answered=stats["total"],
            correct_count=stats["correct"],
            accuracy=(stats["correct"] / stats["total"]) if stats["total"] > 0 else 0
        ) for category, stats in category_stats.items()
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