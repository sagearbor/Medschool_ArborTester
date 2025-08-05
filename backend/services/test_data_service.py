from backend.schemas import AnalyticsSummary, DisciplinePerformance

def get_demo_analytics_data(group_by: str = "disciplines") -> AnalyticsSummary:
    """
    Returns a hardcoded list of performance data for demonstration.
    Data changes based on the grouping dimension selected.
    """
    
    demo_datasets = {
        "disciplines": [
            DisciplinePerformance(discipline="Cardiology", total_answered=25, correct_count=20, accuracy=0.80),
            DisciplinePerformance(discipline="Pulmonology", total_answered=30, correct_count=21, accuracy=0.70),
            DisciplinePerformance(discipline="Biochemistry", total_answered=15, correct_count=6, accuracy=0.40),
            DisciplinePerformance(discipline="Anatomy", total_answered=40, correct_count=38, accuracy=0.95),
            DisciplinePerformance(discipline="Pharmacology", total_answered=22, correct_count=15, accuracy=0.68),
            DisciplinePerformance(discipline="Pathology", total_answered=18, correct_count=14, accuracy=0.78),
        ],
        
        "body_systems": [
            DisciplinePerformance(discipline="Cardiovascular", total_answered=35, correct_count=28, accuracy=0.80),
            DisciplinePerformance(discipline="Respiratory", total_answered=25, correct_count=20, accuracy=0.80),
            DisciplinePerformance(discipline="Neurological", total_answered=30, correct_count=18, accuracy=0.60),
            DisciplinePerformance(discipline="Gastrointestinal", total_answered=22, correct_count=19, accuracy=0.86),
            DisciplinePerformance(discipline="Musculoskeletal", total_answered=15, correct_count=12, accuracy=0.80),
            DisciplinePerformance(discipline="Endocrine", total_answered=12, correct_count=8, accuracy=0.67),
        ],
        
        "specialties": [
            DisciplinePerformance(discipline="Internal Medicine", total_answered=45, correct_count=36, accuracy=0.80),
            DisciplinePerformance(discipline="Emergency Medicine", total_answered=20, correct_count=16, accuracy=0.80),
            DisciplinePerformance(discipline="Pediatrics", total_answered=25, correct_count=22, accuracy=0.88),
            DisciplinePerformance(discipline="Surgery", total_answered=15, correct_count=9, accuracy=0.60),
            DisciplinePerformance(discipline="Psychiatry", total_answered=10, correct_count=8, accuracy=0.80),
            DisciplinePerformance(discipline="Radiology", total_answered=8, correct_count=6, accuracy=0.75),
        ],
        
        "question_type": [
            DisciplinePerformance(discipline="Diagnosis", total_answered=60, correct_count=45, accuracy=0.75),
            DisciplinePerformance(discipline="Treatment", total_answered=35, correct_count=28, accuracy=0.80),
            DisciplinePerformance(discipline="Mechanism", total_answered=20, correct_count=12, accuracy=0.60),
            DisciplinePerformance(discipline="Prevention", total_answered=15, correct_count=13, accuracy=0.87),
            DisciplinePerformance(discipline="Prognosis", total_answered=8, correct_count=6, accuracy=0.75),
        ],
        
        "age_group": [
            DisciplinePerformance(discipline="Adult", total_answered=85, correct_count=68, accuracy=0.80),
            DisciplinePerformance(discipline="Child", total_answered=30, correct_count=24, accuracy=0.80),
            DisciplinePerformance(discipline="Elderly", total_answered=20, correct_count=14, accuracy=0.70),
            DisciplinePerformance(discipline="Neonate", total_answered=8, correct_count=6, accuracy=0.75),
        ],
        
        "acuity": [
            DisciplinePerformance(discipline="Life-threatening", total_answered=15, correct_count=12, accuracy=0.80),
            DisciplinePerformance(discipline="Urgent", total_answered=35, correct_count=25, accuracy=0.71),
            DisciplinePerformance(discipline="Semi-urgent", total_answered=45, correct_count=36, accuracy=0.80),
            DisciplinePerformance(discipline="Routine", total_answered=60, correct_count=48, accuracy=0.80),
            DisciplinePerformance(discipline="Preventive", total_answered=18, correct_count=15, accuracy=0.83),
        ],
        
        "pathophysiology": [
            DisciplinePerformance(discipline="Infectious", total_answered=40, correct_count=32, accuracy=0.80),
            DisciplinePerformance(discipline="Autoimmune", total_answered=20, correct_count=14, accuracy=0.70),
            DisciplinePerformance(discipline="Neoplastic", total_answered=25, correct_count=18, accuracy=0.72),
            DisciplinePerformance(discipline="Genetic", total_answered=15, correct_count=10, accuracy=0.67),
            DisciplinePerformance(discipline="Metabolic", total_answered=18, correct_count=15, accuracy=0.83),
            DisciplinePerformance(discipline="Degenerative", total_answered=12, correct_count=9, accuracy=0.75),
            DisciplinePerformance(discipline="Traumatic", total_answered=8, correct_count=7, accuracy=0.88),
        ]
    }
    
    # Return the appropriate dataset based on group_by parameter
    demo_data = demo_datasets.get(group_by, demo_datasets["disciplines"])
    return AnalyticsSummary(performance_by_discipline=demo_data)