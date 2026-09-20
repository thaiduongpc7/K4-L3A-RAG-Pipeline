"""
Task 3 — Chuẩn hóa dữ liệu sang Markdown.

Hướng dẫn:
    1. Dùng MarkItDown để convert PDF/DOCX.
    2. Đọc JSON và giữ metadata ở đầu file Markdown.
    3. Giữ cấu trúc thư mục legal/ và news/.
    4. Không tạo file rỗng hoặc file trùng khi chạy lại.

Cài đặt:
    Dependency MarkItDown đã được khai báo trong pyproject.toml.
    
-> Hoặc dùng công cụ nào bạn quen khác Markitdown
"""

from pathlib import Path

import json
from markitdown import MarkItDown


LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs() -> None:
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)
    converter = MarkItDown()
    for path in sorted((LANDING_DIR / "legal").iterdir()):
        if path.suffix.lower() not in {".pdf", ".doc", ".docx"}:
            continue
        content = converter.convert(str(path)).text_content.strip()
        if not content:
            raise ValueError(f"No text extracted from {path.name}")
        header = (
            f"# {path.stem}\n\n**Source:** {path.name}\n\n"
            f"**Format:** {path.suffix[1:].upper()}\n\n"
            f"**Original size:** {path.stat().st_size} bytes\n\n---\n\n"
            "**Extraction:** Text extracted from the original document with MarkItDown.\n\n"
        )
        (output_dir / f"{path.stem}.md").write_text(header + content + "\n", encoding="utf-8")


def convert_news_articles() -> None:
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted((LANDING_DIR / "news").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        required = {"url", "title", "date_crawled", "content_markdown"}
        if required - data.keys():
            raise ValueError(f"{path.name} is missing required metadata")
        header = (
            f"# {data['title']}\n\n**Source:** {data['url']}\n\n"
            f"**Crawled:** {data['date_crawled']}\n\n---\n\n"
        )
        (output_dir / f"{path.stem}.md").write_text(
            header + str(data["content_markdown"]).strip() + "\n", encoding="utf-8"
        )


def convert_all() -> None:
    """Convert toàn bộ dữ liệu landing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    convert_legal_docs()
    convert_news_articles()
    print(f"Saved Markdown to: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()