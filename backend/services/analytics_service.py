import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from backend.models import User, Question, Response
from backend.database import get_db

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        pass
    
    def log_question_generation(self, user_id: int, question_id: int, specialty: str, difficulty: str, tokens_used: int):
        """Log question generation event for analytics"""
        logger.info(f"ANALYTICS: Question generated - User: {user_id}, Question: {question_id}, Specialty: {specialty}, Difficulty: {difficulty}, Tokens: {tokens_used}")
    
    def log_answer_submission(self, user_id: int, question_id: int, is_correct: bool, response_time_ms: Optional[int] = None):
        """Log answer submission event for analytics"""
        logger.info(f"ANALYTICS: Answer submitted - User: {user_id}, Question: {question_id}, Correct: {is_correct}, ResponseTime: {response_time_ms}ms")
    
    def log_user_session(self, user_id: int, session_duration_minutes: int, questions_answered: int):
        """Log user session summary for analytics"""
        logger.info(f"ANALYTICS: Session ended - User: {user_id}, Duration: {session_duration_minutes}min, Questions: {questions_answered}")
    
    def get_user_performance_stats(self, user_id: int, db: Session, days: int = 30) -> Dict:
        """Get comprehensive user performance statistics"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total questions answered
            total_responses = db.query(Response).filter(
                and_(Response.user_id == user_id, Response.created_at >= cutoff_date)
            ).count()
            
            # Correct answers
            correct_responses = db.query(Response).filter(
                and_(
                    Response.user_id == user_id,
                    Response.is_correct == True,
                    Response.created_at >= cutoff_date
                )
            ).count()
            
            # Performance by specialty
            specialty_stats = db.query(
                Question.discipline,
                func.count(Response.id).label('total'),
                func.sum(func.cast(Response.is_correct, db.Integer)).label('correct')
            ).join(Response).filter(
                and_(Response.user_id == user_id, Response.created_at >= cutoff_date)
            ).group_by(Question.discipline).all()
            
            # Performance by difficulty
            difficulty_stats = db.query(
                Question.difficulty,
                func.count(Response.id).label('total'),
                func.sum(func.cast(Response.is_correct, db.Integer)).label('correct')
            ).join(Response).filter(
                and_(Response.user_id == user_id, Response.created_at >= cutoff_date)
            ).group_by(Question.difficulty).all()
            
            # Recent activity (last 7 days)
            recent_cutoff = datetime.utcnow() - timedelta(days=7)
            daily_activity = db.query(
                func.date(Response.created_at).label('date'),
                func.count(Response.id).label('questions_answered'),
                func.sum(func.cast(Response.is_correct, db.Integer)).label('correct_answers')
            ).filter(
                and_(Response.user_id == user_id, Response.created_at >= recent_cutoff)
            ).group_by(func.date(Response.created_at)).all()
            
            overall_accuracy = (correct_responses / total_responses * 100) if total_responses > 0 else 0
            
            stats = {
                "user_id": user_id,
                "period_days": days,
                "total_questions": total_responses,
                "correct_answers": correct_responses,
                "overall_accuracy": round(overall_accuracy, 1),
                "specialty_performance": [
                    {
                        "specialty": stat.discipline,
                        "total": stat.total,
                        "correct": stat.correct or 0,
                        "accuracy": round((stat.correct or 0) / stat.total * 100, 1) if stat.total > 0 else 0
                    }
                    for stat in specialty_stats
                ],
                "difficulty_performance": [
                    {
                        "difficulty": stat.difficulty,
                        "total": stat.total,
                        "correct": stat.correct or 0,
                        "accuracy": round((stat.correct or 0) / stat.total * 100, 1) if stat.total > 0 else 0
                    }
                    for stat in difficulty_stats
                ],
                "daily_activity": [
                    {
                        "date": activity.date.isoformat(),
                        "questions_answered": activity.questions_answered,
                        "correct_answers": activity.correct_answers or 0,
                        "accuracy": round((activity.correct_answers or 0) / activity.questions_answered * 100, 1) if activity.questions_answered > 0 else 0
                    }
                    for activity in daily_activity
                ]
            }
            
            logger.info(f"Generated performance stats for user {user_id}: {overall_accuracy}% accuracy over {days} days")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating user performance stats: {str(e)}")
            return {
                "user_id": user_id,
                "error": "Unable to generate performance statistics",
                "total_questions": 0,
                "overall_accuracy": 0
            }
    
    def get_system_usage_stats(self, db: Session, days: int = 30) -> Dict:
        """Get system-wide usage statistics"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total users active in period
            active_users = db.query(func.count(func.distinct(Response.user_id))).filter(
                Response.created_at >= cutoff_date
            ).scalar()
            
            # Total questions generated/answered
            total_questions = db.query(func.count(Response.id)).filter(
                Response.created_at >= cutoff_date
            ).scalar()
            
            # Most popular specialties
            popular_specialties = db.query(
                Question.discipline,
                func.count(Response.id).label('usage_count')
            ).join(Response).filter(
                Response.created_at >= cutoff_date
            ).group_by(Question.discipline).order_by(
                func.count(Response.id).desc()
            ).limit(10).all()
            
            stats = {
                "period_days": days,
                "active_users": active_users,
                "total_questions_answered": total_questions,
                "avg_questions_per_user": round(total_questions / active_users, 1) if active_users > 0 else 0,
                "popular_specialties": [
                    {"specialty": spec.discipline, "usage_count": spec.usage_count}
                    for spec in popular_specialties
                ]
            }
            
            logger.info(f"Generated system usage stats: {active_users} active users, {total_questions} questions answered")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating system usage stats: {str(e)}")
            return {"error": "Unable to generate system statistics"}

analytics_service = AnalyticsService()