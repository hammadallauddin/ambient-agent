# Email Assistant

An ambient AI agent that manages your email with Gmail integration, human-in-the-loop (HITL) review, and memory capabilities.

## Features

- **Email Triage**: Automatically classifies emails as respond, ignore, or notify
- **Human-in-the-Loop**: Review and edit AI-drafted emails before sending
- **Memory**: Learns from your feedback to improve over time
- **Gmail Integration**: Connects directly to Gmail API
- **Calendar Integration**: Schedules meetings via Google Calendar

## Quick Start

### 1. Install Dependencies

```bash
# Using uv (recommended)
pip install uv
uv sync

# Or using pip
pip install -e .
```

### 2. Set Up Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
GOOGLE_API_KEY=your_google_genai_key
```

### 3. Run the Agent

```bash
# Start LangGraph server
langgraph dev

# Or run directly with Python
python -c "from email_assistant.email_assistant_hitl_memory_gmail import email_assistant; print(email_assistant)"
```

## Project Structure

```
src/email_assistant/
├── email_assistant_hitl_memory_gmail.py  # Main agent with Gmail + HITL + Memory
├── cron.py                                # Cron job for email ingestion
├── prompts.py                             # System prompts
├── schemas.py                             # Data schemas
├── utils.py                              # Utility functions
└── tools/
    ├── base.py                          # Tool factory
    ├── default/                         # Default email/calendar tools
    └── gmail/                          # Gmail API integration
        ├── gmail_tools.py              # Gmail API tools
        ├── run_ingest.py              # Email ingestion script
        ├── setup_gmail.py             # Gmail OAuth setup
        └── setup_cron.py              # Cron job setup
```

## Usage Examples

### Using with Gmail

1. Set up Gmail credentials:

```bash
python src/email_assistant/tools/gmail/setup_gmail.py
```

2. Run email ingestion:

```bash
python src/email_assistant/tools/gmail/run_ingest.py --email your@email.com --minutes-since 60
```

### Running with Agent Inbox

For human-in-the-loop review:

1. Start LangGraph server: `langgraph dev`
2. Access Agent Inbox at https://dev.agentinbox.ai
3. Configure your deployment URL and graph name

## Configuration

The agent uses Gemini 2.0 Flash by default. You can modify the model in `email_assistant_hitl_memory_gmail.py`:

```python
llm = init_chat_model(model="gemini-2.0-flash", model_provider="google_genai", temperature=0.0)
```

## Deployment

Deploy to LangGraph Platform:

```bash
langgraph deploy
```

See `src/email_assistant/tools/gmail/README.md` for detailed deployment instructions.

## Dependencies

- langchain >= 1.0.0
- langchain-core >= 1.0.0
- langchain-google-genai >= 1.0.0
- langgraph >= 1.0.0
- google-api-python-client >= 2.128.0
- python-dotenv
- rich
- dateutil
- html2text
