import requests
import json

def test_api():
    """Example client to test the Help Desk API"""
    base_url = "http://localhost:8000"
    
    # Check system configuration
    try:
        config_response = requests.get(f"{base_url}/config")
        if config_response.status_code == 200:
            config = config_response.json()
            print(f"System Configuration:")
            print(f"  LLM Provider: {config['provider']}")
            print(f"  Model: {config['model']}")
            print(f"  Configured: {config['configured']}")
            print()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API server. Make sure it's running on localhost:8000")
        return
    
    # Test requests
    test_requests = [
        "I forgot my password and can't log in",
        "My laptop screen is completely black",
        "I think my computer has been hacked"
    ]
    
    print("Testing Help Desk API")
    print("=" * 40)
    
    for i, request_text in enumerate(test_requests, 1):
        print(f"\nTest {i}: {request_text}")
        
        # Make API request
        response = requests.post(
            f"{base_url}/support",
            json={"request": request_text}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Category: {result['classification']['category']}")
            print(f"Confidence: {result['classification']['confidence']:.2f}")
            print(f"Escalate: {result['escalate']}")
            print(f"Response: {result['response'][:100]}...")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_api()