"""Build the vector index from ./data and persist it to ./storage.

Usage:
    uv run python index_documents.py
"""
import shutil
from pathlib import Path

from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex

from core_settings import configure_runtime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"


def main() -> None:
    configure_runtime()

    if STORAGE_DIR.exists():
        shutil.rmtree(STORAGE_DIR)

    # 1. Load corporate documents from the data folder
    docs = SimpleDirectoryReader(DATA_DIR).load_data()
    print(f"Loaded {len(docs)} document(s) from {DATA_DIR}")

    # 2. Create embeddings and index the text (in-memory)
    index = VectorStoreIndex.from_documents(docs)

    # 3. Persist the index to storage so the app can load it later
    index.storage_context.persist(persist_dir=str(STORAGE_DIR))
    print(f"Index persisted to {STORAGE_DIR}")


if __name__ == "__main__":
    main()