"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"
LEGAL_EXTENSIONS = {".pdf", ".doc", ".docx"}


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Validate collected originals without replacing them on reruns."""
    documents = sorted(
        path for path in DATA_DIR.iterdir()
        if path.is_file() and not path.name.startswith(".")
        and path.suffix.lower() in LEGAL_EXTENSIONS and path.stat().st_size > 1024
    )
    if len(documents) < 3:
        raise RuntimeError("Need at least 3 PDF/DOC/DOCX files in data/landing/legal/")
    for path in documents:
        print(f"Ready: {path.name} ({path.stat().st_size} bytes)")
    print(f"Validated {len(documents)} legal source documents")


if __name__ == "__main__":
    setup_directory()
    download_documents()