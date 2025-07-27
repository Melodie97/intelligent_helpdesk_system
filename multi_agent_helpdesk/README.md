# Multi-Agent Help Desk System

A LangGraph-based multi-agent system for intelligent help desk automation.

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

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in parent `.env` file:
```
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

3. Run the system:
```bash
python main.py
```

## Key Features

- **State Management**: LangGraph manages workflow state between agents
- **Specialized Agents**: Each agent has a specific responsibility
- **Flexible Routing**: Workflow adapts based on escalation decisions
- **Reusable Components**: Agents can be easily modified or replaced

## Comparison with Original System

| Feature | Original | Multi-Agent |
|---------|----------|-------------|
| Architecture | Monolithic | Agent-based |
| Coordination | Sequential | Graph-based |
| Extensibility | Limited | High |
| State Management | Manual | Automatic |
| Error Handling | Basic | Agent-level |

## Usage

```python
from workflows.helpdesk_workflow import HelpDeskWorkflow

helpdesk = HelpDeskWorkflow()
result = helpdesk.process_request("I can't reset my password")
print(result['response'])
```