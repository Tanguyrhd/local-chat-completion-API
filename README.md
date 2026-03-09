# Local Chat Completion API

A local REST API built on top of [Ollama](https://ollama.com) that abstracts the LLM backend behind a clean, extensible interface. Designed to support future features like tool use, web search, and thinking mode — without being tied to any specific LLM provider.

## Features

- **Simple responses** — `POST /v1/responses` with optional system instructions
- **Streaming** — token-by-token responses via Server-Sent Events (`"stream": true`)
- **Model listing** — `GET /v1/models` lists all locally available Ollama models
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
| `DEFAULT_MODEL` | `tinyllama`                       | Model used when none is specified     |
| `API_KEY`       | _(none)_                          | If set, all requests require this key |

Authentication is disabled when `API_KEY` is not set.

## Running

**Locally:**

```bash
make run
```

**With Docker (API + Ollama):**

```bash
make docker-build
make docker-up

# First time only — pull a model inside the Ollama container
docker compose exec ollama ollama pull llama3.2:3b

make docker-down   # stop when done
```

The API starts at `http://localhost:8000`. Interactive docs available at `http://localhost:8000/docs`.

---

## API Reference

### POST `/v1/responses`

Simple endpoint — one input string, optional system instruction.

| Field          | Type    | Required | Default         | Description                      |
|----------------|---------|----------|-----------------|----------------------------------|
| `input`        | string  | yes      | -               | The user's message               |
| `model`        | string  | no       | `DEFAULT_MODEL` | Ollama model to use              |
| `instructions` | string  | no       | -               | System-level instruction         |
| `temperature`  | float   | no       | `0.7`           | Sampling temperature (0.0 - 1.0) |
| `stream`       | boolean | no       | `false`         | Stream response token by token   |

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

**Streaming example:**

```bash
curl -N -X POST http://localhost:8000/v1/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Tell me a story", "stream": true}'
```

```text
data: {"model": "tinyllama", "temperature": 0.7, "stream": true}

data: {"content": "Once"}

data: {"content": " upon"}

data: {"content": " a time"}

data: [DONE]
```

---

### GET `/v1/models`

List all models currently available on the local Ollama server.

```bash
curl http://localhost:8000/v1/models
```

```json
{
  "models": [
    {"id": "llama3.2:3b", "size": 2019393189},
    {"id": "tinyllama:latest", "size": 637875785}
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

| File                           | What it tests                        |
|--------------------------------|--------------------------------------|
| `test_prompt_builder.py`       | Pure unit tests — message formatting |
| `test_responses.py`            | `/v1/responses` with mock            |
| `test_security.py`             | API key authentication               |
| `integration/`                 | Real Ollama calls (opt-in)           |

---

## Project Structure

```text
app/
├── main.py                  # FastAPI app entry point
├── endpoints/
│   ├── responses.py         # POST /v1/responses
│   └── models.py            # GET /v1/models
├── core/
│   ├── security.py          # API key authentication
│   ├── config.py            # Environment-based configuration
│   └── logging.py           # Logging setup
├── schemas/
│   └── responses.py         # Pydantic request/response models
└── services/
    ├── llm_engine.py        # Orchestration layer
    ├── ollama_client.py     # HTTP client for Ollama
    └── prompt_builder.py    # Message list construction
tests/
├── conftest.py              # Shared fixtures
├── endpoints/
│   └── test_responses.py
├── core/
│   └── test_security.py
├── services/
│   └── test_prompt_builder.py
└── integration/
    └── test_integration.py
```
