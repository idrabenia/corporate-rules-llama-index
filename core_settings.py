"""Shared model configuration for index_documents.py and app.py.

Embeddings run locally on-device (FastEmbed) and the LLM is served by
Ollama running in Docker on localhost (see README.md for the docker
command). No API keys required.
"""
from llama_index.core import Settings
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.llms.ollama import Ollama

CACHE_DIR = "model_cache"
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5-Q"

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:latest"


def configure_runtime() -> None:
    Settings.embed_model = FastEmbedEmbedding(
        model_name=EMBED_MODEL,
        cache_dir=CACHE_DIR,
    )
    Settings.llm = Ollama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL,
        request_timeout=300.0,
    )