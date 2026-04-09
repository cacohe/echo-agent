# Echo - Personal Reflection and Decision AI

Echo is an AI assistant that captures your daily碎片化 thoughts, emotions, and decisions through low-friction voice/text input, then provides insights, pattern recognition, and decision support across months and years.

## Features

- **Low-friction input**: Voice or text recording with minimal friction
- **Implicit association**: AI automatically finds connections between current and past records
- **Pattern recognition**: Discover emotional and behavioral patterns you weren't aware of
- **Decision support**: Get objective snapshots from your history when facing decisions
- **Proactive reminders**: AI proactively reminds you based on your past entries

## Quick Start

### Backend

```bash
# Install dependencies
uv venv
uv add fastapi uvicorn pydantic openai chromadb sqlite-utils apscheduler python-multipart httpx pytest pytest-asyncio

# Run server
python -m src.main
```

### LLM Provider Configuration

Echo supports both **OpenAI** and **MiniMax** as LLM providers.

#### Using OpenAI (default)

```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_MODEL="gpt-4o-mini"  # optional, default is gpt-4o-mini
```

#### Using MiniMax

```bash
export LLM_PROVIDER=minimax
export MINIMAX_API_KEY="your-minimax-api-key"
export MINIMAX_MODEL="M2-her"  # optional, default is M2-her
```

MiniMax provides competitive pricing and good Chinese language support. Get your API key from [MiniMax Platform](https://platform.minimaxi.com/).

### API Endpoints

- `POST /api/records` - Create a new record
- `GET /api/records` - Get recent records
- `GET /api/insights/weekly` - Get weekly insight report
- `GET /api/insights/reminders` - Get active reminders

### Frontend (Coming Soon)

A mobile app is planned for easier voice input and push notifications.

## Architecture

```
src/
├── api/           # REST API endpoints
├── core/          # Core processing engine
├── memory/        # SQLite + ChromaDB storage
├── llm/           # LLM client wrappers (OpenAI, MiniMax)
└── models/        # Pydantic data models
```

## License

MIT
