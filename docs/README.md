# Intelligent Help Desk System

A modular AI-powered help desk system that classifies user requests, retrieves relevant solutions from a knowledge base, and generates contextual responses using LLM APIs.

## Architecture

```
├── src/
│   ├── core/                 # Core business logic
│   │   ├── models.py         # Data models
│   │   ├── classifier.py     # Request classification
│   │   ├── knowledge_retriever.py  # Knowledge base search
│   │   ├── escalation_engine.py    # Escalation logic
│   │   └── help_desk_system.py     # Main orchestrator
│   ├── llm/                  # LLM integration
│   │   └── response_generator.py   # Response generation
│   └── api/                  # REST API
│       └── routes.py         # FastAPI routes
├── config/
│   └── settings.py           # Configuration management
├── data/                     # Knowledge base files
├── tests/                    # Test modules
├── scripts/                  # Utility scripts
└── docs/                     # Documentation
```

## Features

- **Request Classification**: TF-IDF based categorization into 7 predefined types
- **Knowledge Retrieval**: Vector search through comprehensive knowledge base
- **Response Generation**: Contextual responses using Gemini (default) or OpenAI
- **Escalation Logic**: Rule-based escalation for complex issues
- **REST API**: FastAPI interface with automatic documentation
- **Modular Design**: Clean separation of concerns for easy extension

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure LLM Provider**
   ```bash
   python scripts/setup_llm.py
   ```

3. **Run the System**
   ```bash
   python run_server.py
   ```

4. **Test the System**
   ```bash
   python tests/test_system.py
   ```

## LLM Provider Options

- **Gemini (Default)**: Google's Gemini Pro model
  - Free tier available
  - Get API key: https://makersuite.google.com/app/apikey
  
- **OpenAI**: GPT-3.5-turbo model
  - Paid API required
  - Get API key: https://platform.openai.com/api-keys

## API Endpoints

- **POST /support** - Process help desk request
- **GET /health** - Health check
- **GET /categories** - Get available categories
- **GET /config** - Get current LLM configuration

## Testing

- `python tests/test_config.py` - Test configuration without API keys
- `python tests/test_system.py` - Full system evaluation
- `python scripts/client_example.py` - API client example

## Performance

The system processes requests in ~1-2 seconds and achieves high accuracy on the provided test dataset with proper LLM configuration.