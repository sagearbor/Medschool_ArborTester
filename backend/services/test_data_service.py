from backend.schemas import AnalyticsSummary, DisciplinePerformance

def get_demo_analytics_data() -> AnalyticsSummary:
    """
    Returns a hardcoded list of performance data for demonstration.
    """
    demo_data = [
        DisciplinePerformance(discipline="Cardiology", total_answered=25, correct_count=20, accuracy=0.80),
        DisciplinePerformance(discipline="Pulmonology", total_answered=30, correct_count=21, accuracy=0.70),
        DisciplinePerformance(discipline="Biochemistry", total_answered=15, correct_count=6, accuracy=0.40),
        DisciplinePerformance(discipline="Anatomy", total_answered=40, correct_count=38, accuracy=0.95),
        DisciplinePerformance(discipline="Pharmacology", total_answered=22, correct_count=15, accuracy=0.68),
    ]
    
    return AnalyticsSummary(performance_by_discipline=demo_data)