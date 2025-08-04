import pytest
from backend.models import Question, Response

def test_analytics_summary_returns_correct_aggregations(authenticated_client, db_session):
    client, user = authenticated_client

    q1 = Question(content="Cardiology Question", discipline="Cardiology")
    q2 = Question(content="Biochemistry Question", discipline="Biochemistry")
    db_session.add_all([q1, q2])
    db_session.commit()

    responses = [
        Response(user_id=user.id, question_id=q1.id, user_answer="A", is_correct=True),
        Response(user_id=user.id, question_id=q1.id, user_answer="B", is_correct=True),
        Response(user_id=user.id, question_id=q1.id, user_answer="C", is_correct=False),
        Response(user_id=user.id, question_id=q2.id, user_answer="D", is_correct=True),
    ]
    db_session.add_all(responses)
    db_session.commit()

    response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 200
    data = response.json()["performance_by_discipline"]
    
    assert len(data) == 2
    
    cardio_stats = next((item for item in data if item["discipline"] == "Cardiology"), None)
    biochem_stats = next((item for item in data if item["discipline"] == "Biochemistry"), None)

    assert cardio_stats is not None
    assert cardio_stats["total_answered"] == 3
    assert cardio_stats["correct_count"] == 2
    assert pytest.approx(cardio_stats["accuracy"]) == 2/3

    assert biochem_stats is not None
    assert biochem_stats["total_answered"] == 1
    assert biochem_stats["correct_count"] == 1
    assert biochem_stats["accuracy"] == 1.0