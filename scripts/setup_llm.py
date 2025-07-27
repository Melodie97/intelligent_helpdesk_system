#!/usr/bin/env python3
"""
Setup script to configure LLM provider for the Help Desk System
"""
import os

def setup_llm():
    print("Intelligent Help Desk System - LLM Configuration")
    print("=" * 50)
    
    # Choose provider
    print("Available LLM providers:")
    print("1. Gemini (Google) - Default, free tier available")
    print("2. OpenAI (GPT-3.5-turbo) - Requires paid API key")
    
    while True:
        choice = input("\nSelect provider (1 or 2): ").strip()
        if choice in ['1', '2']:
            break
        print("Please enter 1 or 2")
    
    provider = 'gemini' if choice == '1' else 'openai'
    
    # Get API key
    if provider == 'gemini':
        print("\nTo get a Gemini API key:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        api_key = input("Enter your Gemini API key: ").strip()
    else:
        print("\nTo get an OpenAI API key:")
        print("1. Go to https://platform.openai.com/api-keys")
        print("2. Create a new API key")
        api_key = input("Enter your OpenAI API key: ").strip()
    
    # Update .env file
    env_content = f"""# LLM Configuration - Choose one
LLM_PROVIDER={provider}

# API Keys
GEMINI_API_KEY={api_key if provider == 'gemini' else 'your_gemini_api_key_here'}
OPENAI_API_KEY={api_key if provider == 'openai' else 'your_openai_api_key_here'}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Configuration saved!")
    print(f"Provider: {provider}")
    print(f"API key configured: {'Yes' if api_key else 'No'}")
    print("\nYou can now run the system with: python run_server.py")

if __name__ == "__main__":
    setup_llm()