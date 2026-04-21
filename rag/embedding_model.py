from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TRANSFORMERS_NO_TF", "1")
os.environ.setdefault("USE_TF", "0")

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_CACHE_DIR = (
    Path.home()
    / ".cache"
    / "huggingface"
    / "hub"
    / "models--sentence-transformers--all-MiniLM-L6-v2"
    / "snapshots"
)


def get_local_model_path() -> Path | None:
    if not MODEL_CACHE_DIR.exists():
        return None

    snapshots = sorted(
        [path for path in MODEL_CACHE_DIR.iterdir() if path.is_dir()],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return snapshots[0] if snapshots else None


def load_embedding_model() -> SentenceTransformer:
    local_model_path = get_local_model_path()

    if local_model_path is not None:
        return SentenceTransformer(str(local_model_path), local_files_only=True)

    return SentenceTransformer(MODEL_NAME)
