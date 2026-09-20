"""Task 6 — Lexical search bằng BM25.

Dùng cùng corpus chunks với Task 5. BM25 phù hợp với từ khóa chính xác, mã tài
liệu và tên riêng. Output phải theo SearchResult và sort score giảm dần.
"""

import re

from .task4_chunking_indexing import chunk_documents, load_documents


CORPUS: list[dict] = []


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)


def build_bm25_index(corpus: list[dict]):
    """Tạo BM25 index từ cùng corpus chunks của Task 4."""
    from rank_bm25 import BM25Okapi
    return BM25Okapi([_tokenize(item["content"]) for item in corpus])


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """Trả về BM25 SearchResult theo score giảm dần."""
    if top_k <= 0 or not query.strip():
        return []
    corpus = CORPUS or chunk_documents(load_documents())
    if not corpus:
        return []
    scores = build_bm25_index(corpus).get_scores(_tokenize(query))
    indices = sorted(range(len(corpus)), key=lambda index: scores[index], reverse=True)[:top_k]
    return [
        {
            "id": corpus[index]["id"],
            "content": corpus[index]["content"],
            "score": float(scores[index]),
            "metadata": corpus[index]["metadata"],
            "retrieval_method": "bm25",
        }
        for index in indices
    ]


if __name__ == "__main__":
    for result in lexical_search("test query", top_k=3):
        print(result)