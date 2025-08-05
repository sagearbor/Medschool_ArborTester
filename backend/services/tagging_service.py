import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class TaggingBackend(ABC):
    """Abstract base class for different LLM backends used for question tagging"""
    
    @abstractmethod
    def tag_question(self, question_content: str, question_options: Dict) -> Dict:
        """Tag a medical question with structured categories"""
        pass

class AzureOpenAITagger(TaggingBackend):
    """Azure OpenAI backend for question tagging"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    
    def tag_question(self, question_content: str, question_options: Dict) -> Dict:
        """Tag question using Azure OpenAI"""
        
        system_prompt = """You are a medical education expert. Analyze the given medical question and categorize it using the structured taxonomy below.

Return ONLY a JSON object with these exact keys:

{
    "disciplines": ["anatomy", "physiology", "biochemistry", "pharmacology", "pathology", "microbiology", "immunology", "histology", "embryology", "genetics", "biostatistics", "ethics", "behavioral_sciences"],
    "body_systems": ["cardiovascular", "respiratory", "gastrointestinal", "genitourinary", "neurological", "musculoskeletal", "endocrine", "integumentary", "hematologic", "reproductive", "immune", "sensory"],
    "specialties": ["internal_medicine", "surgery", "pediatrics", "ob_gyn", "psychiatry", "emergency", "family_medicine", "radiology", "pathology", "anesthesiology", "dermatology", "ophthalmology", "orthopedics", "neurology", "cardiology"],
    "question_type": "diagnosis|treatment|mechanism|prevention|prognosis|anatomy|normal_vs_abnormal",
    "age_group": "neonate|infant|child|adolescent|adult|elderly",
    "acuity": "life_threatening|urgent|semi_urgent|routine|preventive",
    "pathophysiology": ["infectious", "neoplastic", "autoimmune", "genetic", "metabolic", "degenerative", "traumatic", "toxic", "congenital", "iatrogenic"]
}

Select only the most relevant 1-3 items for list fields. Use null for any category that doesn't clearly apply."""

        user_prompt = f"""Question: {question_content}

Options: {json.dumps(question_options) if question_options else 'None'}

Categorize this medical question:"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            tags_json = response.choices[0].message.content.strip()
            tags_data = json.loads(tags_json)
            
            logger.info(f"Tagged question - Tokens: {response.usage.total_tokens}")
            return tags_data
            
        except Exception as e:
            logger.error(f"Error tagging question: {str(e)}")
            return self._get_fallback_tags()
    
    def _get_fallback_tags(self) -> Dict:
        """Return basic fallback tags if tagging fails"""
        return {
            "disciplines": ["general_medicine"],
            "body_systems": ["general"],
            "specialties": ["internal_medicine"],
            "question_type": "diagnosis",
            "age_group": "adult",
            "acuity": "routine",
            "pathophysiology": []
        }

class LocalLLMTagger(TaggingBackend):
    """Local LLM backend for question tagging (placeholder for future implementation)"""
    
    def __init__(self):
        # TODO: Initialize local model (Ollama, etc.)
        self.model_endpoint = os.getenv("LOCAL_LLM_ENDPOINT", "http://localhost:11434")
        logger.info("LocalLLMTagger initialized - not yet implemented")
    
    def tag_question(self, question_content: str, question_options: Dict) -> Dict:
        """Tag question using local LLM (placeholder)"""
        logger.warning("Local LLM tagging not yet implemented, using fallback")
        return {
            "disciplines": ["general_medicine"],
            "body_systems": ["general"],
            "specialties": ["internal_medicine"],
            "question_type": "diagnosis",
            "age_group": "adult",
            "acuity": "routine",
            "pathophysiology": []
        }

class QuestionTaggingService:
    """Main service for tagging medical questions with configurable backends"""
    
    def __init__(self, backend_type: str = "azure_openai"):
        self.backend = self._create_backend(backend_type)
        logger.info(f"QuestionTaggingService initialized with {backend_type} backend")
    
    def _create_backend(self, backend_type: str) -> TaggingBackend:
        """Factory method to create the appropriate tagging backend"""
        if backend_type == "azure_openai":
            return AzureOpenAITagger()
        elif backend_type == "local_llm":
            return LocalLLMTagger()
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")
    
    def tag_question(self, question_content: str, question_options: Dict = None) -> Dict:
        """Tag a medical question with structured categories"""
        try:
            tags = self.backend.tag_question(question_content, question_options or {})
            
            # Validate and clean the tags
            cleaned_tags = self._validate_tags(tags)
            return cleaned_tags
            
        except Exception as e:
            logger.error(f"Error in question tagging: {str(e)}")
            return self._get_emergency_fallback()
    
    def _validate_tags(self, tags: Dict) -> Dict:
        """Validate and clean the returned tags"""
        # Ensure all expected keys exist
        expected_keys = [
            "disciplines", "body_systems", "specialties", 
            "question_type", "age_group", "acuity", "pathophysiology"
        ]
        
        for key in expected_keys:
            if key not in tags:
                tags[key] = [] if key in ["disciplines", "body_systems", "specialties", "pathophysiology"] else None
        
        return tags
    
    def _get_emergency_fallback(self) -> Dict:
        """Emergency fallback if all tagging fails"""
        return {
            "disciplines": ["general_medicine"],
            "body_systems": ["general"],
            "specialties": ["internal_medicine"],
            "question_type": "diagnosis",
            "age_group": "adult", 
            "acuity": "routine",
            "pathophysiology": []
        }

# Lazy-loaded singleton instance
_tagging_service = None

def get_tagging_service() -> QuestionTaggingService:
    """Get the singleton tagging service instance (lazy-loaded)"""
    global _tagging_service
    if _tagging_service is None:
        backend_type = os.getenv("TAGGING_BACKEND", "azure_openai")
        _tagging_service = QuestionTaggingService(backend_type)
    return _tagging_service