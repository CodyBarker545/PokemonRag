from __future__ import annotations

import json
import sys
from pathlib import Path

import faiss
import numpy as np

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag.embedding_model import MODEL_NAME, load_embedding_model
from rag.preprocess import chunk_documents, load_documents


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = PROJECT_ROOT / "vector_store"
INDEX_PATH = INDEX_DIR / "pokemon_rag.index"
CHUNKS_PATH = INDEX_DIR / "chunks.json"


def embed_chunks(chunks: list[str], model_name: str = MODEL_NAME) -> np.ndarray:
    model = load_embedding_model()
    embeddings = model.encode(
        chunks,
        batch_size=16,
        convert_to_numpy=True,
        show_progress_bar=True,
    )

    embeddings = embeddings.astype("float32")
    faiss.normalize_L2(embeddings)
    return embeddings


def build_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    return index


def save_chunk_records(chunks) -> None:
    records = [
        {
            "id": position,
            "text": chunk.text,
            "metadata": chunk.metadata,
        }
        for position, chunk in enumerate(chunks)
    ]

    CHUNKS_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")


def main() -> None:
    documents = load_documents()
    chunks = chunk_documents(documents)
    chunk_texts = [chunk.text for chunk in chunks]

    if not chunks:
        raise ValueError("No chunks were created. Check that RAGDocs contains .txt files.")

    print(f"Loaded {len(documents)} documents")
    print(f"Created {len(chunks)} chunks")
    print(f"Embedding model: {MODEL_NAME}")

    embeddings = embed_chunks(chunk_texts)
    index = build_index(embeddings)

    INDEX_DIR.mkdir(exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))
    save_chunk_records(chunks)

    print()
    print("FAISS index built successfully")
    print(f"Index vectors: {index.ntotal}")
    print(f"Embedding dimension: {index.d}")
    print(f"Saved index: {INDEX_PATH}")
    print(f"Saved chunk metadata/text: {CHUNKS_PATH}")


if __name__ == "__main__":
    main()
