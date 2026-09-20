"""
Task 2 — Crawl bài viết/thông báo.

Hướng dẫn:
    1. Điền tối thiểu 5 URL công khai vào ARTICLE_URLS.
    2. Crawl từng URL bằng Crawl4AI.
    3. Lưu mỗi bài thành một JSON trong data/landing/news/.
    4. Giữ đủ url, title, date_crawled và content_markdown.

Cài browser trước khi chạy:
    python -m playwright install chromium
    
-> Dùng Firecrawl or bất cứ công cụ nào bạn quen    
"""

import asyncio
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import requests


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"

ARTICLE_URLS = [
    "https://www.momo.vn/blog/top-khach-san-ninh-binh-c101dt266",
    "https://www.bestprice.vn/blog/diem-den-8/ninh-binh-255/kinh-nghiem-di-chuyen-khi-di-du-lich-ninh-binh-day-du-nhat_2-4939.html",
    "https://mia.vn/cam-nang-du-lich/top-5-nhung-dia-diem-hot-mua-sam-tai-ninh-binh-3421",
    "https://vnexpress.net/cam-nang-du-lich-ninh-binh-4127327.html",
    "https://www.momo.vn/blog/top-mon-ngon-ninh-binh-c101dt267",
    "https://www.momo.vn/blog/kinh-nghiem-du-lich-ninh-binh-c101dt237",
]


class ArticleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.blocks: list[tuple[str, str]] = []
        self.current_tag: str | None = None
        self.current_text: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "nav", "footer", "header"}:
            self.skip_depth += 1
        elif not self.skip_depth and tag in {"title", "h1", "h2", "h3", "p", "li"}:
            self.current_tag = tag
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if not self.skip_depth and self.current_tag:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "nav", "footer", "header"}:
            self.skip_depth = max(0, self.skip_depth - 1)
        elif tag == self.current_tag:
            text = re.sub(r"\s+", " ", "".join(self.current_text)).strip()
            if text:
                (self.title_parts if tag == "title" else self.blocks).append(
                    text if tag == "title" else (tag, text)
                )
            self.current_tag = None
            self.current_text = []


def _to_markdown(html: str) -> tuple[str, str]:
    parser = ArticleParser()
    parser.feed(html)
    title = parser.title_parts[0] if parser.title_parts else "Ninh Bình"
    seen: set[str] = set()
    lines = []
    for tag, text in parser.blocks:
        if len(text) < 25 or text in seen:
            continue
        seen.add(text)
        lines.append(f"- {text}" if tag == "li" else text)
    return title, "\n\n".join(lines)


async def crawl_article(url: str) -> dict:
    response = await asyncio.to_thread(
        requests.get, url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; RAG coursework crawler)"},
        timeout=30,
    )
    response.raise_for_status()
    title, markdown = _to_markdown(response.text)
    if len(markdown) < 200:
        raise ValueError("Page did not contain enough readable article content")
    return {
        "url": url,
        "title": title,
        "date_crawled": datetime.now(timezone.utc).isoformat(),
        "content_markdown": markdown,
    }


async def crawl_all() -> None:
    """Crawl và lưu từng bài thành một file JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for index, url in enumerate(ARTICLE_URLS, 1):
        try:
            article = await crawl_article(url)
            output = DATA_DIR / f"article_{index:02d}.json"
            output.write_text(
                json.dumps(article, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"Saved: {output}")
        except Exception as error:
            print(f"Failed: {url} — {error}")


if __name__ == "__main__":
    asyncio.run(crawl_all())