import os
from typing import Literal

LLMProvider = Literal["gemini", "openai"]

class Config:
    """Configuration management for the Help Desk System"""
    
    def __init__(self):
        self.llm_provider: LLMProvider = os.getenv('LLM_PROVIDER', 'gemini').lower()
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Data paths
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.categories_file = os.path.join(self.data_dir, 'categories.json')
        self.knowledge_base_file = os.path.join(self.data_dir, 'knowledge_base.md')
        self.troubleshooting_file = os.path.join(self.data_dir, 'troubleshooting_database.json')
        self.installation_guides_file = os.path.join(self.data_dir, 'installation_guides.json')
        self.policies_file = os.path.join(self.data_dir, 'company_it_policies.md')
        self.test_requests_file = os.path.join(self.data_dir, 'test_requests.json')
    
    def validate(self) -> bool:
        """Validate configuration based on selected provider"""
        if self.llm_provider == 'gemini':
            if not self.gemini_api_key:
                print("Error: GEMINI_API_KEY not found in environment")
                return False
        elif self.llm_provider == 'openai':
            if not self.openai_api_key:
                print("Error: OPENAI_API_KEY not found in environment")
                return False
        else:
            print(f"Error: Unsupported LLM provider: {self.llm_provider}")
            return False
        
        return True
    
    def get_provider_info(self) -> dict:
        """Get information about the current provider"""
        return {
            "provider": self.llm_provider,
            "model": "gemini-pro" if self.llm_provider == "gemini" else "gpt-3.5-turbo",
            "configured": self.validate()
        }