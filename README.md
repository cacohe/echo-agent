# Echo - Personal Reflection and Decision AI

Echo is an AI assistant that captures your daily碎片化 thoughts, emotions, and decisions through low-friction voice/text input, then provides insights, pattern recognition, and decision support across months and years.

## Features

- **Low-friction input**: Voice or text recording with minimal friction
- **Implicit association**: AI automatically finds connections between current and past records
- **Pattern recognition**: Discover emotional and behavioral patterns you weren't aware of
- **Decision support**: Get objective snapshots from your history when facing decisions
- **Proactive reminders**: AI proactively reminds you based on your past entries

## Quick Start

### 1. Install Dependencies

```bash
uv venv
uv add fastapi uvicorn pydantic openai chromadb sqlite-utils apscheduler python-multipart httpx pytest pytest-asyncio python-dotenv
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Choose LLM provider: "openai" or "minimax"
LLM_PROVIDER=minimax

# MiniMax API (recommended for Chinese)
MINIMAX_API_KEY=your-minimax-api-key
MINIMAX_MODEL=M2-her

# Or OpenAI (default)
# OPENAI_API_KEY=your-openai-api-key
# OPENAI_MODEL=gpt-4o-mini
```

### 3. Run Server

```bash
python -m src.main
```

The server will start at `http://localhost:8000`

### LLM Provider

Echo supports both **OpenAI** and **MiniMax**:

| Provider | Model | Chinese Support | Price |
|----------|-------|-----------------|-------|
| MiniMax (recommended) | M2-her | Excellent | Lower |
| OpenAI | gpt-4o-mini | Good | Higher |

Get your MiniMax API key from [MiniMax Platform](https://platform.minimaxi.com/).

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
