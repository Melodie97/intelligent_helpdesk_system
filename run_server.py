#!/usr/bin/env python3
"""
Simple script to run the Help Desk API server
"""
import uvicorn
from dotenv import load_dotenv
from src.api.routes import create_app

if __name__ == "__main__":
    load_dotenv()
    
    print("Starting Intelligent Help Desk System...")
    print("API will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)