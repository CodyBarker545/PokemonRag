from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import faiss
import numpy as np

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from rag.build_faiss_index import CHUNKS_PATH, INDEX_PATH, MODEL_NAME
from rag.embedding_model import load_embedding_model


def load_chunk_records(path: Path = CHUNKS_PATH) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def embed_query(query: str, model_name: str = MODEL_NAME) -> np.ndarray:
    model = load_embedding_model()
    embedding = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(embedding)
    return embedding


def search(query: str, top_k: int = 3) -> list[tuple[float, dict]]:
    if not INDEX_PATH.exists() or not CHUNKS_PATH.exists():
        raise FileNotFoundError("Run python -m rag.build_faiss_index before searching.")

    index = faiss.read_index(str(INDEX_PATH))
    records = load_chunk_records()
    query_embedding = embed_query(query)

    scores, ids = index.search(query_embedding, top_k)
    results: list[tuple[float, dict]] = []

    for score, record_id in zip(scores[0], ids[0]):
        if record_id == -1:
            continue
        results.append((float(score), records[int(record_id)]))

    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the Pokemon RAG FAISS index.")
    parser.add_argument("query", help="Question or search query to retrieve chunks for.")
    parser.add_argument("--top-k", type=int, default=3, help="Number of chunks to retrieve.")
    args = parser.parse_args()

    results = search(args.query, args.top_k)

    print(f"Query: {args.query}")
    print(f"Top {len(results)} retrieved chunks")
    print("=" * 40)

    for rank, (score, record) in enumerate(results, start=1):
        metadata = record["metadata"]
        print(
            f"{rank}. Score: {score:.4f} | "
            f"Source: {metadata['filename']} | "
            f"Chunk: {metadata['chunk_index']}"
        )
        print(record["text"][:900])
        if len(record["text"]) > 900:
            print("...")
        print()


if __name__ == "__main__":
    main()
