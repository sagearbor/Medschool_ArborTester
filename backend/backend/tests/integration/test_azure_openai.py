#!/usr/bin/env python3
"""
Quick test script to verify Azure OpenAI integration works
"""
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.append('/mnt/c/Users/scb2/AppData/Local/GitHubDesktop/app-3.4.20/Medschool_ArborTester/backend')

try:
    from services.openai_service import OpenAIService
    
    print("🧪 Testing Azure OpenAI Integration...")
    print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    print(f"Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
    print(f"API Version: {os.getenv('AZURE_OPENAI_API_VERSION')}")
    print()
    
    # Initialize service
    openai_service = OpenAIService()
    
    # Test question generation
    print("📋 Generating clinical question...")
    question_data = openai_service.generate_clinical_question(
        specialty="Cardiology",
        difficulty="Intermediate"
    )
    
    print("✅ Success! Generated question:")
    print(f"Question: {question_data['question'][:100]}...")
    print(f"Options: {list(question_data['options'].keys())}")
    print(f"Correct Answer: {question_data['correct_answer']}")
    print(f"Tokens Used: {question_data['tokens_used']}")
    print()
    
    # Test answer evaluation
    print("💬 Testing answer evaluation...")
    feedback = openai_service.evaluate_answer(
        question=question_data['question'],
        correct_answer=question_data['correct_answer'],
        user_answer="B",  # Assume wrong answer
        explanation=question_data['explanation']
    )
    
    print("✅ Feedback generated:")
    print(f"Feedback: {feedback['feedback']}")
    print()
    
    print("🎉 Azure OpenAI integration is working correctly!")
    
except Exception as e:
    print(f"❌ Error testing Azure OpenAI: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()