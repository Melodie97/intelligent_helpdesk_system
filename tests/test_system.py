import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.help_desk_system import HelpDeskSystem
from src.core.models import HelpDeskRequest
from config.settings import Config

def test_system():
    """Test the help desk system with provided test requests"""
    system = HelpDeskSystem()
    config = Config()
    
    # Load test requests
    with open(config.test_requests_file, 'r') as f:
        test_data = json.load(f)
    
    results = []
    correct_classifications = 0
    correct_escalations = 0
    
    print("Testing Help Desk System")
    print("=" * 50)
    
    for test_case in test_data['test_requests']:
        request = HelpDeskRequest(request=test_case['request'])
        response = system.process_request(request)
        
        # Check classification accuracy
        classification_correct = response.classification.category.value == test_case['expected_classification']
        if classification_correct:
            correct_classifications += 1
        
        # Check escalation accuracy
        escalation_correct = response.escalate == test_case['escalate']
        if escalation_correct:
            correct_escalations += 1
        
        results.append({
            'id': test_case['id'],
            'request': test_case['request'],
            'expected_category': test_case['expected_classification'],
            'actual_category': response.classification.category.value,
            'classification_correct': classification_correct,
            'confidence': response.classification.confidence,
            'expected_escalate': test_case['escalate'],
            'actual_escalate': response.escalate,
            'escalation_correct': escalation_correct,
            'response': response.response[:100] + "..." if len(response.response) > 100 else response.response
        })
        
        print(f"Request {test_case['id']}: {test_case['request'][:50]}...")
        print(f"  Category: {response.classification.category.value} (confidence: {response.classification.confidence:.2f})")
        print(f"  Escalate: {response.escalate}")
        print(f"  Response: {response.response[:100]}...")
        print()
    
    # Calculate metrics
    total_tests = len(test_data['test_requests'])
    classification_accuracy = correct_classifications / total_tests
    escalation_accuracy = correct_escalations / total_tests
    
    print("=" * 50)
    print("RESULTS SUMMARY")
    print("=" * 50)
    print(f"Total tests: {total_tests}")
    print(f"Classification accuracy: {classification_accuracy:.2%} ({correct_classifications}/{total_tests})")
    print(f"Escalation accuracy: {escalation_accuracy:.2%} ({correct_escalations}/{total_tests})")
    
    return results

if __name__ == "__main__":
    test_system()