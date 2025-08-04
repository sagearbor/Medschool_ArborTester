import os
import logging
from typing import Dict, List, Optional
from openai import AzureOpenAI
from datetime import datetime

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    
    def generate_clinical_question(self, 
                                 specialty: str = "General Medicine",
                                 difficulty: str = "Intermediate",
                                 question_type: str = "Multiple Choice") -> Dict:
        """
        Generate a clinical board-style question using Azure OpenAI
        """
        system_prompt = f"""You are a medical education expert creating {difficulty.lower()} level {specialty} questions for medical board exam preparation. 

Create a realistic clinical scenario question with:
- A clear patient presentation
- Relevant clinical details
- {question_type} format with 4-5 options (A, B, C, D, E if needed)
- One correct answer with explanation
- Plausible distractors

Format your response as JSON:
{{
    "question": "Clinical scenario and question text",
    "options": {{
        "A": "Option A text",
        "B": "Option B text", 
        "C": "Option C text",
        "D": "Option D text"
    }},
    "correct_answer": "A",
    "explanation": "Detailed explanation of why the correct answer is right and others are wrong",
    "difficulty": "{difficulty}",
    "specialty": "{specialty}",
    "topics": ["topic1", "topic2"]
}}"""

        user_prompt = f"Generate a {difficulty.lower()} {specialty} clinical question for medical board exam preparation."
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Log the API call for analytics
            logger.info(f"Generated question - Specialty: {specialty}, Difficulty: {difficulty}, Tokens: {response.usage.total_tokens}")
            
            import json
            question_data = json.loads(response.choices[0].message.content)
            question_data["generated_at"] = datetime.utcnow().isoformat()
            question_data["tokens_used"] = response.usage.total_tokens
            
            return question_data
            
        except Exception as e:
            logger.error(f"Error generating question: {str(e)}")
            raise Exception(f"Failed to generate question: {str(e)}")
    
    def evaluate_answer(self, question: str, correct_answer: str, user_answer: str, explanation: str) -> Dict:
        """
        Use AI to provide detailed feedback on user's answer
        """
        system_prompt = """You are a medical educator providing feedback on student answers. 
        Be encouraging but precise in your feedback."""
        
        user_prompt = f"""
        Question: {question}
        Correct Answer: {correct_answer}
        Student Answer: {user_answer}
        Explanation: {explanation}
        
        Provide personalized feedback on the student's answer choice, including:
        - Whether they got it right or wrong
        - Key learning points
        - Areas for improvement if incorrect
        
        Keep response concise but educational (2-3 sentences).
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return {
                "feedback": response.choices[0].message.content,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            logger.error(f"Error generating feedback: {str(e)}")
            return {"feedback": "Unable to generate personalized feedback at this time."}