from src.workflows.helpdesk_workflow import HelpDeskWorkflow
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Initialize the multi-agent workflow
    helpdesk = HelpDeskWorkflow()
    
    print("Multi-Agent Help Desk System")
    print("=" * 40)
    
    while True:
        user_request = input("\nEnter your help desk request (or 'quit' to exit): ")
        
        if user_request.lower() == 'quit':
            break
        
        try:
            # Process the request through the multi-agent workflow
            result = helpdesk.process_request(user_request)
            
            print(f"\nCategory: {result['classification'].category.value}")
            print(f"Confidence: {result['classification'].confidence:.2f}")
            print(f"Escalated: {result['escalate']}")
            if result['escalation_reason']:
                print(f"Escalation Reason: {result['escalation_reason']}")
            
            print(f"\nResponse:")
            print(result['response'])
            
            print(f"\nKnowledge Sources Used:")
            for item in result['knowledge_items']:
                print(f"- {item.source} (relevance: {item.relevance_score:.2f})")
                
        except Exception as e:
            print(f"Error processing request: {e}")

if __name__ == "__main__":
    main()