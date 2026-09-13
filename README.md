# LlamaIndex Hello

An example [LlamaIndex](https://www.llamaindex.ai/) project with a FastAPI
backend, a persisted vector index, and a small chat web UI.

- `data/` — corporate documents (employee handbook) used as the knowledge base
- `index_documents.py` — reads `data/`, builds embeddings, persists the index to `storage/`
- `app.py` — FastAPI server exposing a `/api/chat` endpoint
- `static/` — HTML/CSS/JS chat interface served at `/`

## Setup

Requirements: `uv` (https://uv.astral.sh) and Python 3.11+.

```bash
uv sync          # create .venv and install dependencies
uv run python index_documents.py   # build and persist the index
```

The first run downloads the local embedding model
(`nomic-ai/nomic-embed-text-v1.5-Q`) into `model_cache/`, so no API key is
needed for chunking and retrieval. The first server start is slower because the
model is loaded into memory.

## Run

```bash
uv run uvicorn app:app --reload
```

Open http://127.0.0.1:8000 and ask questions such as:

- "How many vacation days do I get?"
- "What is the office safe code?"
- "How do I report a sick day?"

## LLM / Ollama in Docker

The language model used to compose answers (LLaMA) runs locally in an Ollama
Docker container on localhost, so no API keys are needed. Start it once:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3.2:latest   # bigger: llama3.1:8b
```

Then run the app and the API will query `http://localhost:11434`. To use a
different LLaMA model, change `OLLAMA_MODEL` in `core_settings.py` (and pull
it with `ollama pull <name>` first).

# corporate-rules-llama-index