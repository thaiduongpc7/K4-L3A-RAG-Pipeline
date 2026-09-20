"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
import json
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CACHE_PATH = Path(__file__).parent.parent / "pageindex_cache.json"
LEGAL_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def _load_cache() -> dict[str, str]:
    if not CACHE_PATH.exists():
        return {}
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict[str, str]) -> None:
    CACHE_PATH.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    if not PAGEINDEX_API_KEY:
        return
    from pageindex import PageIndexClient

    client = PageIndexClient(PAGEINDEX_API_KEY)
    cache = _load_cache()
    changed = False
    for path in sorted(LEGAL_DIR.glob("*.pdf")):
        cache_key = path.name
        if cache.get(cache_key):
            continue
        response = client.submit_document(str(path))
        doc_id = response.get("doc_id")
        if not doc_id:
            raise RuntimeError(f"PageIndex response missing doc_id for {path.name}")
        cache[cache_key] = str(doc_id)
        changed = True
    if changed:
        _save_cache(cache)


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    if not PAGEINDEX_API_KEY or top_k <= 0 or not query.strip():
        return []
    from pageindex import PageIndexClient

    client = PageIndexClient(PAGEINDEX_API_KEY)
    cache = _load_cache()
    if not cache:
        upload_documents()
        cache = _load_cache()
    results: list[dict] = []
    for source, doc_id in cache.items():
        if not client.is_retrieval_ready(doc_id):
            continue
        submitted = client.submit_query(doc_id, query)
        retrieval_id = submitted.get("retrieval_id")
        if not retrieval_id:
            continue
        response = client.get_retrieval(retrieval_id)
        for rank, node in enumerate(_extract_nodes(response), 1):
            content = _node_content(node)
            if not content:
                continue
            results.append({
                "id": f"pageindex:{doc_id}:{rank}",
                "content": content,
                "score": 1.0 / rank,
                "metadata": {
                    "source": source,
                    "title": Path(source).stem,
                    "doc_type": "legal",
                    "url": None,
                    "chunk_index": rank - 1,
                },
                "retrieval_method": "pageindex",
            })
    return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]


def _extract_nodes(value: object) -> list[dict]:
    if isinstance(value, dict):
        for key in ("nodes", "results", "retrieval_results", "data"):
            child = value.get(key)
            if isinstance(child, list):
                return [item for item in child if isinstance(item, dict)]
        for child in value.values():
            found = _extract_nodes(child)
            if found:
                return found
    elif isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def _node_content(node: dict) -> str:
    for key in ("content", "text", "markdown", "summary"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


if __name__ == "__main__":
    upload_documents()
