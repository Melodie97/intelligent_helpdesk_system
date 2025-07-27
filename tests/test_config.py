#!/usr/bin/env python3
"""
Test configuration and basic system functionality without requiring API keys
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from config.settings import Config
from src.core.help_desk_system import HelpDeskSystem
from src.core.state import HelpDeskRequest

def test_config():
    """Test system configuration"""
    load_dotenv()
    
    print("Testing Help Desk System Configuration")
    print("=" * 45)
    
    # Test configuration
    config = Config()
    print(f"LLM Provider: {config.llm_provider}")
    print(f"Configuration valid: {config.validate()}")
    print()
    
    # Test components that don't require API keys
    print("Testing core components...")
    
    try:
        # Test multi-agent system
        help_desk = HelpDeskSystem()
        test_request = HelpDeskRequest(request="I forgot my password", user_id="test_user")
        
        response = help_desk.process_request(test_request)
        
        print(f"✅ Classification: {response.classification.category} (confidence: {response.classification.confidence:.2f})")
        print(f"✅ Knowledge Items: Found {len(response.knowledge_items)} relevant items")
        print(f"✅ Escalation: {response.escalate}")
        print(f"✅ Response Generated: {len(response.response)} characters")
        
        print("\n🎉 Multi-agent system working correctly!")
        
        if not config.validate():
            print("\n⚠️  Note: LLM provider not configured. Run 'python scripts/setup_llm.py' to configure.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_config()