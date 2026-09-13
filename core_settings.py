"""Shared model configuration for index_documents.py and app.py.

Uses local on-device embeddings (FastEmbed) so no API keys are required
for indexing and retrieval. The language model used to compose answers
still defaults to OpenAI (set OPENAI_API_KEY); see README.md.
"""
from llama_index.core import Settings
from llama_index.embeddings.fastembed import FastEmbedEmbedding

CACHE_DIR = "model_cache"
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5-Q"


def configure_runtime() -> None:
    Settings.embed_model = FastEmbedEmbedding(
        model_name=EMBED_MODEL,
        cache_dir=CACHE_DIR,
    )