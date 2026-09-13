"""FastAPI backend: loads the persisted index and exposes a chat/search UX endpoint.

Usage:
    uv run uvicorn app:app --reload
"""
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from llama_index.core import StorageContext, load_index_from_storage
from pydantic import BaseModel

from core_settings import configure_runtime

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
STATIC_DIR = BASE_DIR / "static"

configure_runtime()

app = FastAPI(title="LlamaIndex Hello")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    source_texts: list[str]


def _get_query_engine():
    if not STORAGE_DIR.exists():
        raise HTTPException(
            status_code=500,
            detail="Index not found. Run `uv run python index_documents.py` first.",
        )
    storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))
    index = load_index_from_storage(storage_context)
    return index.as_query_engine(similarity_top_k=2)


@app.get("/")
def index_page() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question must not be empty")

    query_engine = _get_query_engine()
    response = query_engine.query(payload.question)

    source_texts = [node.node.get_content() for node in response.source_nodes]

    return ChatResponse(answer=str(response), source_texts=source_texts)