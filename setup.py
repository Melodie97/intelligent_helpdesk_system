#!/usr/bin/env python3
"""
Main setup script for the Intelligent Help Desk System
"""
import os
import subprocess
import sys

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def setup_llm():
    """Run LLM configuration"""
    print("\nConfiguring LLM provider...")
    try:
        subprocess.check_call([sys.executable, "scripts/setup_llm.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ LLM configuration failed")
        return False

def test_configuration():
    """Test the system configuration"""
    print("\nTesting system configuration...")
    try:
        subprocess.check_call([sys.executable, "tests/test_config.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Configuration test failed")
        return False

def main():
    print("Intelligent Help Desk System - Setup")
    print("=" * 40)
    
    # Step 1: Install dependencies
    if not install_dependencies():
        return
    
    # Step 2: Configure LLM
    if not setup_llm():
        return
    
    # Step 3: Test configuration
    if not test_configuration():
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the server: python run_server.py")
    print("2. Test the API: python scripts/client_example.py")
    print("3. Run full tests: python tests/test_system.py")

if __name__ == "__main__":
    main()