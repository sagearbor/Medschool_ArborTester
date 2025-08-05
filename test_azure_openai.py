#!/usr/bin/env python3

import os
import sys
sys.path.append('/mnt/c/Users/scb2/AppData/Local/GitHubDesktop/app-3.4.20/Medschool_ArborTester')

from backend.services.openai_service import OpenAIService

def test_azure_openai():
    print("Testing Azure OpenAI connection...")
    print(f"Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    print(f"API Version: {os.getenv('AZURE_OPENAI_API_VERSION')}")
    print(f"Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")
    print(f"API Key: {'*' * 20 if os.getenv('AZURE_OPENAI_API_KEY') else 'NOT SET'}")
    
    try:
        service = OpenAIService()
        result = service.generate_clinical_question(
            specialty="Cardiology",
            difficulty="Intermediate"
        )
        print("SUCCESS: Question generated!")
        print(f"Question: {result['question'][:100]}...")
        return True
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    # Load environment variables from backend/.env
    from dotenv import load_dotenv
    load_dotenv('backend/.env')
    
    success = test_azure_openai()
    sys.exit(0 if success else 1)