import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import uuid

class FileStorage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        self.users_dir = self.data_dir / "users"
        self.questions_dir = self.data_dir / "questions"
        self.responses_dir = self.data_dir / "responses"
        
        for dir_path in [self.users_dir, self.questions_dir, self.responses_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def save_json(self, file_path: Path, data: Dict[str, Any]):
        """Save data to JSON file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_json(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load data from JSON file"""
        if not file_path.exists():
            return None
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    # User operations
    def save_user(self, user_data: Dict[str, Any]) -> str:
        """Save user and return user_id"""
        user_id = user_data.get('id') or str(uuid.uuid4())
        user_data['id'] = user_id
        user_data['created_at'] = user_data.get('created_at', datetime.utcnow().isoformat())
        
        file_path = self.users_dir / f"{user_id}.json"
        self.save_json(file_path, user_data)
        return user_id
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        file_path = self.users_dir / f"{user_id}.json"
        return self.load_json(file_path)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        for user_file in self.users_dir.glob("*.json"):
            user_data = self.load_json(user_file)
            if user_data and user_data.get('email') == email:
                return user_data
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        users = []
        for user_file in self.users_dir.glob("*.json"):
            user_data = self.load_json(user_file)
            if user_data:
                users.append(user_data)
        return users
    
    # Question operations
    def save_question(self, question_data: Dict[str, Any]) -> str:
        """Save question and return question_id"""
        question_id = question_data.get('id') or str(uuid.uuid4())
        question_data['id'] = question_id
        question_data['created_at'] = question_data.get('created_at', datetime.utcnow().isoformat())
        
        file_path = self.questions_dir / f"{question_id}.json"
        self.save_json(file_path, question_data)
        return question_id
    
    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get question by ID"""
        file_path = self.questions_dir / f"{question_id}.json"
        return self.load_json(file_path)
    
    def get_questions_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all questions for a user"""
        questions = []
        for question_file in self.questions_dir.glob("*.json"):
            question_data = self.load_json(question_file)
            if question_data and question_data.get('user_id') == user_id:
                questions.append(question_data)
        return sorted(questions, key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Response operations
    def save_response(self, response_data: Dict[str, Any]) -> str:
        """Save response and return response_id"""
        response_id = response_data.get('id') or str(uuid.uuid4())
        response_data['id'] = response_id
        response_data['created_at'] = response_data.get('created_at', datetime.utcnow().isoformat())
        
        file_path = self.responses_dir / f"{response_id}.json"
        self.save_json(file_path, response_data)
        return response_id
    
    def get_response(self, response_id: str) -> Optional[Dict[str, Any]]:
        """Get response by ID"""
        file_path = self.responses_dir / f"{response_id}.json"
        return self.load_json(file_path)
    
    def get_responses_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all responses for a user"""
        responses = []
        for response_file in self.responses_dir.glob("*.json"):
            response_data = self.load_json(response_file)
            if response_data and response_data.get('user_id') == user_id:
                responses.append(response_data)
        return sorted(responses, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def get_responses_by_question(self, question_id: str) -> List[Dict[str, Any]]:
        """Get all responses for a question"""
        responses = []
        for response_file in self.responses_dir.glob("*.json"):
            response_data = self.load_json(response_file)
            if response_data and response_data.get('question_id') == question_id:
                responses.append(response_data)
        return sorted(responses, key=lambda x: x.get('created_at', ''), reverse=True)

# Global storage instance
storage = FileStorage()