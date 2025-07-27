# Multi-Agent Intelligent Help Desk System

A LangGraph-based multi-agent system for intelligent help desk automation using specialized AI agents.

## Architecture

This system uses **LangGraph** as the coordination framework with specialized agents:

### Agents
- **ClassifierAgent**: Categorizes incoming requests using embeddings
- **KnowledgeAgent**: Retrieves relevant information from knowledge base
- **EscalationAgent**: Determines if human intervention is needed
- **ResponseAgent**: Generates contextual responses using LLM

### Workflow
```
Request → Classify → Retrieve Knowledge → Check Escalation → Generate Response
```

## Project Structure

```
Intelligent Help Desk System/
├── src/
│   ├── agents/                    # Specialized AI agents
│   │   ├── classifier_agent.py    # Request classification
│   │   ├── knowledge_agent.py     # Knowledge retrieval
│   │   ├── escalation_agent.py    # Escalation decisions
│   │   └── response_agent.py      # Response generation
│   ├── workflows/                 # LangGraph coordination
│   │   └── helpdesk_workflow.py   # Main workflow orchestrator
│   ├── core/                      # Core models and system
│   │   ├── state.py              # All data models and state
│   │   └── help_desk_system.py   # Main system interface
│   └── api/                       # FastAPI endpoints
│       └── routes.py             # REST API routes
├── data/                          # Knowledge base and configuration
│   ├── categories.json           # Request categories
│   ├── knowledge_base.md         # Company knowledge base
│   ├── troubleshooting_database.json  # Troubleshooting steps
│   └── company_it_policies.md    # IT policies
├── config/                        # System configuration
│   └── settings.py               # Configuration management
├── tests/                         # Test files
│   ├── test_config.py            # System configuration tests
│   └── test_system.py            # System functionality tests
├── scripts/                       # Utility scripts
│   ├── setup_llm.py              # LLM configuration helper
│   └── client_example.py         # API client example
├── main.py                        # CLI interface
├── run_server.py                  # FastAPI server launcher
├── setup.py                       # Package installation
├── requirements.txt               # Dependencies
└── .env                          # Environment variables
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   # Edit .env with your API keys
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   ```

3. **Run CLI Interface**
   ```bash
   python main.py
   ```

4. **Run API Server**
   ```bash
   python run_server.py
   ```

5. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/support" \
        -H "Content-Type: application/json" \
        -d '{"request": "I forgot my password", "user_id": "john.doe"}'
   ```

## Key Features

- **State Management**: LangGraph manages workflow state between agents
- **Specialized Agents**: Each agent has a specific responsibility
- **Flexible Routing**: Workflow adapts based on escalation decisions
- **Reusable Components**: Agents can be easily modified or replaced
- **Multi-LLM Support**: Compatible with OpenAI GPT and Google Gemini
- **RESTful API**: Easy integration with existing systems

## Configuration

Edit the `.env` file to configure:

- **LLM Provider**: Choose between `openai` or `gemini`
- **API Keys**: Set your provider's API key
- **SMTP Settings**: For email escalation notifications (optional)

## API Endpoints

- `POST /support` - Process support request
- `GET /health` - Health check
- `GET /categories` - Available request categories
- `GET /config` - Current configuration

## Testing

```bash
python tests/test_config.py
```

## Usage

```python
from src.workflows.helpdesk_workflow import HelpDeskWorkflow

helpdesk = HelpDeskWorkflow()
result = helpdesk.process_request("I can't reset my password")
print(result['response'])
```

## Comparison with Traditional Systems

| Feature | Traditional | Multi-Agent |
|---------|-------------|-------------|
| Architecture | Monolithic | Agent-based |
| Coordination | Sequential | Graph-based |
| Extensibility | Limited | High |
| State Management | Manual | Automatic |
| Error Handling | Basic | Agent-level |

## Development

The system is modular and extensible:

- Add new categories in `data/categories.json`
- Extend knowledge base in `data/knowledge_base.md`
- Customize escalation rules in `src/agents/escalation_agent.py`
- Modify response templates in `src/agents/response_agent.py`
- Create new agents by following the existing agent patterns