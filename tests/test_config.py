#!/usr/bin/env python3
"""
Test configuration and basic system functionality without requiring API keys
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
from config.settings import Config
from src.core.classifier import RequestClassifier
from src.core.knowledge_retriever import KnowledgeRetriever
from src.core.escalation_engine import EscalationEngine

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
        # Test classifier
        classifier = RequestClassifier()
        test_request = "I forgot my password"
        classification = classifier.classify(test_request)
        print(f"✅ Classifier: {classification.category} (confidence: {classification.confidence:.2f})")
        
        # Test knowledge retriever
        retriever = KnowledgeRetriever()
        knowledge = retriever.retrieve(test_request, classification.category, top_k=2)
        print(f"✅ Knowledge Retriever: Found {len(knowledge)} relevant items")
        
        # Test escalation engine
        escalation = EscalationEngine()
        should_escalate, reason = escalation.should_escalate(test_request, classification)
        print(f"✅ Escalation Engine: Escalate={should_escalate}")
        
        print("\n🎉 Core system components working correctly!")
        
        if not config.validate():
            print("\n⚠️  Note: LLM provider not configured. Run 'python scripts/setup_llm.py' to configure.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_config()