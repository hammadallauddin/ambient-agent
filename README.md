# Ambient Agent

An intelligent email assistant built with LangGraph that uses AI to triage and respond to emails with human-in-the-loop capabilities.

## Project Structure

```
ambient-agent/
├── src/
│   └── email_assistant/
│       ├── __init__.py
│       ├── email_assistant_hitl_memory_gmail.py  # Main email assistant workflow
│       ├── prompts.py                           # System prompts and instructions
│       ├── schemas.py                          # Data schemas and types
│       ├── utils.py                            # Utility functions
│       ├── cron.py                            # Cron job setup
│       └── tools/                             # Tool implementations
│           ├── __init__.py
│           ├── base.py                        # Base tool classes
│           ├── default/                       # Default tool implementations
│           └── gmail/                         # Gmail-specific tools
├── tests/                                     # Test files
│   ├── test_basic_functionality.py           # Basic functionality tests
│   ├── test_components.py                    # Component tests
│   ├── test_email_assistant.py               # Email assistant tests
│   ├── test_final_verification.py            # Final verification tests
│   ├── test_gemini_25_flash.py               # Gemini model tests
│   ├── test_simple_triage.py                 # Simple triage tests
│   ├── test_with_api_key.py                  # API key tests
│   ├── test_with_store.py                    # Memory store tests
│   ├── test_workflow_mock.py                 # Workflow mock tests
│   └── test_working_version.py               # Working version tests
├── .env.example                              # Environment variables template
├── .env                                      # Environment variables
├── pyproject.toml                           # Project configuration
└── README.md                                # This file
```

## Features

- **Email Triage**: Automatically classify emails as respond, ignore, or notify
- **Human-in-the-Loop**: Review and edit AI-generated responses before sending
- **Memory Management**: Learn from user preferences and feedback
- **Gmail Integration**: Full Gmail API integration for email operations
- **Calendar Integration**: Schedule meetings and check availability

## Configuration

Copy `.env.example` to `.env` and configure the following environment variables:

```bash
GOOGLE_API_KEY=your_api_key
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT="ambient-agent"
GOOGLE_MODEL=gemini-2.5-flash
```

## Usage

```python
from email_assistant.email_assistant_hitl_memory_gmail import email_assistant
from langgraph.store.memory import InMemoryStore

# Create a store for memory
store = InMemoryStore()

# Process an email
result = email_assistant.invoke({
    "email_input": {
        "from": "sender@example.com",
        "to": "recipient@example.com",
        "subject": "Meeting Request",
        "body": "Can we meet tomorrow?",
        "id": "email_id_123"
    }
}, config={"configurable": {"thread_id": "thread_123"}}, store=store)
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

## Requirements

- Python 3.10+
- Google API Key
- LangSmith API Key (optional for tracing)
- Gmail API credentials (for Gmail integration)