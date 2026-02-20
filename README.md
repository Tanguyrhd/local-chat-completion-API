# Local Chat Completion API

An OpenAI-compatible REST API that runs locally using [Ollama](https://ollama.com). Drop-in replacement for OpenAI's `/v1/chat/completions` endpoint, with an additional simpler `/v1/responses` endpoint.

## Features

- **OpenAI-compatible** — `POST /v1/chat/completions` with full message history support
- **Simple responses** — `POST /v1/responses` with optional system instructions
- **Multiple completions** — generate `n` independent responses in one request
- **Temperature control** — tune creativity vs determinism
- **Optional API key auth** — secure with `x-api-key` header
- **100% local** — no data leaves your machine

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) running locally

```bash
# Pull a model (examples)
ollama pull llama3.2      # recommended default (~2GB)
ollama pull tinyllama     # lightweight for testing (~600MB)
```

## Installation

```bash
# Clone the project
git clone <repo-url>
cd local-chat-completion-API

# Install dependencies
make install

# Copy and configure environment
cp .env.example .env
```

## Configuration

Edit `.env` to match your setup:

| Variable        | Default                           | Description                           |
|-----------------|-----------------------------------|---------------------------------------|
| `OLLAMA_URL`    | `http://localhost:11434/api/chat` | Ollama API endpoint                   |
| `DEFAULT_MODEL` | `llama3`                          | Model used when none is specified     |
| `API_KEY`       | _(none)_                          | If set, all requests require this key |

Authentication is disabled when `API_KEY` is not set.

## Running

```bash
make run
```

The API starts at `http://localhost:8000`. Interactive docs available at `http://localhost:8000/docs`.

---

## API Reference

### POST `/v1/responses`

Simple endpoint — one input string, optional system instruction.

| Field          | Type   | Required | Default         | Description                      |
|----------------|--------|----------|-----------------|----------------------------------|
| `input`        | string | yes      | -               | The user's message               |
| `model`        | string | no       | `DEFAULT_MODEL` | Ollama model to use              |
| `instructions` | string | no       | -               | System-level instruction         |
| `temperature`  | float  | no       | `0.7`           | Sampling temperature (0.0 - 1.0) |

Example:

```bash
curl -X POST http://localhost:8000/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "instructions": "You are a pirate. Always respond in pirate speak.",
    "input": "What is the weather like today?"
  }'
```

```json
{
  "model": "llama3.2",
  "output": {
    "role": "assistant",
    "content": "Arrr, the skies be grey and the winds be howlin'..."
  }
}
```

---

### POST `/v1/chat/completions`

OpenAI-compatible endpoint — accepts a full conversation history.

| Field         | Type    | Required | Default         | Description                      |
|---------------|---------|----------|-----------------|----------------------------------|
| `messages`    | array   | yes      | -               | Conversation history             |
| `model`       | string  | no       | `DEFAULT_MODEL` | Ollama model to use              |
| `n`           | integer | no       | `1`             | Number of completions to generate|
| `temperature` | float   | no       | `0.7`           | Sampling temperature (0.0 - 1.0) |

Each message: `{"role": "system"|"user"|"assistant", "content": "..."}`

Example:

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

```json
{
  "model": "llama3.2",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "The capital of France is Paris."
      }
    }
  ]
}
```

---

### Authentication

When `API_KEY` is set, add the `x-api-key` header to every request:

```bash
curl -X POST http://localhost:8000/v1/responses \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-secret-key" \
  -d '{"input": "Hello"}'
```

---

## Tests

```bash
# Run all tests (no Ollama required)
make test

# Run integration tests (Ollama must be running)
make test-all

# With coverage
pytest --cov=app -m "not integration"
```

| File                           | What it tests                         |
|--------------------------------|---------------------------------------|
| `test_prompt_builder.py`       | Pure unit tests — message formatting  |
| `test_routes_chat.py`          | `/v1/chat/completions` with mock      |
| `test_routes_responses.py`     | `/v1/responses` with mock             |
| `test_auth.py`                 | API key authentication                |
| `integration/`                 | Real Ollama calls (opt-in)            |

---

## Project Structure

```text
app/
├── main.py                  # FastAPI app entry point
├── api/
│   ├── routes_chat.py       # POST /v1/chat/completions
│   └── routes_responses.py  # POST /v1/responses
├── core/
│   ├── security.py          # API key authentication
│   └── config/
│       └── settings.py      # Environment-based configuration
├── models/
│   ├── chat.py              # Request models for /chat/completions
│   └── response.py          # Request/response models for /responses
├── services/
│   ├── llm_engine.py        # Orchestration layer
│   └── ollama_client.py     # HTTP client for Ollama
└── utils/
    └── prompt_builder.py    # Message list construction
tests/
├── conftest.py              # Shared fixtures
├── test_prompt_builder.py
├── test_routes_chat.py
├── test_routes_responses.py
├── test_auth.py
└── integration/
    └── test_integration.py
```
