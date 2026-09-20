"""
Task 4 — Chunking, embedding và indexing.

Hướng dẫn:
    1. Đọc toàn bộ Markdown trong data/standardized/.
    2. Chia văn bản bằng strategy đã chọn.
    3. Embed chunks bằng một provider duy nhất.
    4. Upsert vào ChromaDB với cosine distance.

Mỗi document/chunk phải theo docs/MODULE_CONTRACTS.md. ID cần ổn định để
chạy lại pipeline không tạo dữ liệu trùng. Task 5 phải dùng chung embed_texts().
"""

import os
from pathlib import Path

from dotenv import load_dotenv


STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# Giải thích lựa chọn tham số trong báo cáo nhóm.
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

COLLECTION_NAME = "rag_documents"
load_dotenv()
_embedding_model = None


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    provider = os.getenv("EMBEDDING_PROVIDER", "sentence_transformers").lower()
    if provider != "sentence_transformers":
        raise ValueError(f"Unsupported embedding provider: {provider}")
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(
            os.getenv("EMBEDDING_MODEL", EMBEDDING_MODEL)
        )
    return _embedding_model.encode(
        texts, normalize_embeddings=True, show_progress_bar=False
    ).tolist()


def get_collection():
    """Mở Chroma collection dùng cosine distance."""
    import chromadb
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )


def load_documents() -> list[dict]:
    """Đọc Markdown và trả về danh sách Document."""
    documents = []
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        relative_path = path.relative_to(STANDARDIZED_DIR)
        doc_type = relative_path.parts[0]
        if doc_type not in {"legal", "news"}:
            continue
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            continue
        title = next(
            (line[2:].strip() for line in content.splitlines() if line.startswith("# ")),
            path.stem,
        )
        source_line = next(
            (line for line in content.splitlines() if line.startswith("**Source:**")),
            "",
        )
        source_value = source_line.removeprefix("**Source:**").strip()
        documents.append({
            "id": relative_path.as_posix(),
            "content": content,
            "metadata": {
                "source": path.name,
                "title": title,
                "doc_type": doc_type,
                "url": source_value if source_value.startswith("http") else None,
            },
        })
    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Chia Document thành chunks có id và chunk_index."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = []
    for document in documents:
        for index, text in enumerate(splitter.split_text(document["content"])):
            if text.strip():
                chunks.append({
                    "id": f"{document['id']}::chunk-{index}",
                    "content": text,
                    "metadata": {**document["metadata"], "chunk_index": index},
                })
    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Thêm embedding vào từng chunk."""
    vectors = embed_texts([chunk["content"] for chunk in chunks])
    if len(vectors) != len(chunks):
        raise ValueError("Embedding count does not match chunk count")
    for chunk, vector in zip(chunks, vectors):
        chunk["embedding"] = vector
    return chunks


def index_to_vectorstore(chunks: list[dict]) -> None:
    """Upsert chunks vào ChromaDB."""
    if not chunks:
        return
    get_collection().upsert(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["content"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks],
    )


def run_pipeline() -> None:
    """Chạy load, chunk, embed và index."""
    documents = load_documents()
    chunks = chunk_documents(documents)
    embedded_chunks = embed_chunks(chunks)
    index_to_vectorstore(embedded_chunks)
    print(f"Indexed {len(embedded_chunks)} chunks")


if __name__ == "__main__":
    run_pipeline()