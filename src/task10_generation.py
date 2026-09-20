"""
Task 10 — Generation có citation.

Hướng dẫn:
    1. Retrieve top-k chunks.
    2. Reorder để giảm lost-in-the-middle.
    3. Format context kèm title và source.
    4. Gọi provider được chọn trong .env.
    5. Trả answer, sources và retrieval_source.

Nếu context không đủ hoặc provider lỗi, trả safe refusal; không bịa thông tin.
"""

import os
from collections.abc import Iterator

from dotenv import load_dotenv

from .task9_retrieval_pipeline import retrieve


load_dotenv()

TOP_K = 5
TOP_P = 0.9
TEMPERATURE = 0.3

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "")

SYSTEM_PROMPT = """Trả lời chỉ từ context được cung cấp.
Mỗi khẳng định phải có citation. Nếu thiếu evidence, hãy từ chối xác minh."""


def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """Đưa chunks quan trọng về đầu và cuối context."""
    if len(chunks) <= 2:
        return list(chunks)
    front = chunks[::2]
    back = chunks[1::2]
    return front + back[::-1]


def format_context(chunks: list[dict]) -> str:
    """Tạo context có title và source label."""
    parts = []
    for index, chunk in enumerate(chunks, 1):
        metadata = chunk["metadata"]
        parts.append(
            f"[Document {index} | Title: {metadata['title']} | "
            f"Source: {metadata['source']}]\n{chunk['content']}"
        )
    return "\n\n---\n\n".join(parts)


def call_llm(system_prompt: str, user_message: str) -> str:
    """Gọi OpenAI, Gemini hoặc Anthropic theo cấu hình."""
    if not LLM_MODEL:
        raise RuntimeError("LLM_MODEL is not configured")
    if LLM_PROVIDER == "openai":
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url is None and api_key and api_key.startswith("sk-or-"):
            base_url = "https://openrouter.ai/api/v1"
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=LLM_MODEL,
            max_tokens=1024,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""
    if LLM_PROVIDER == "anthropic":
        from anthropic import Anthropic

        response = Anthropic().messages.create(
            model=LLM_MODEL,
            max_tokens=1024,
            temperature=TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return "".join(block.text for block in response.content if hasattr(block, "text"))
    if LLM_PROVIDER == "gemini":
        from google import genai

        response = genai.Client().models.generate_content(
            model=LLM_MODEL,
            contents=f"{system_prompt}\n\n{user_message}",
        )
        return response.text or ""
    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")


def stream_llm(system_prompt: str, user_message: str) -> Iterator[str]:
    """Yield provider output chunks for Streamlit's token-by-token rendering."""
    if not LLM_MODEL:
        raise RuntimeError("LLM_MODEL is not configured")
    if LLM_PROVIDER == "openai":
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url is None and api_key and api_key.startswith("sk-or-"):
            base_url = "https://openrouter.ai/api/v1"
        response = OpenAI(api_key=api_key, base_url=base_url).chat.completions.create(
            model=LLM_MODEL,
            max_tokens=1024,
            temperature=TEMPERATURE,
            stream=True,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        for chunk in response:
            text = chunk.choices[0].delta.content if chunk.choices else None
            if text:
                yield text
        return
    if LLM_PROVIDER == "gemini":
        from google import genai

        response = genai.Client().models.generate_content_stream(
            model=LLM_MODEL,
            contents=f"{system_prompt}\n\n{user_message}",
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
        return
    raise RuntimeError("Streaming is supported for OpenAI-compatible and Gemini providers")


def stream_generation_with_citation(query: str, top_k: int = TOP_K) -> tuple[Iterator[str], list[dict]]:
    """Return a token stream and its grounded sources for the Streamlit UI."""
    chunks = retrieve(query, top_k=top_k)
    if not chunks:
        return iter(["Tôi không thể xác minh thông tin này từ nguồn hiện có."]), []
    context = format_context(reorder_for_llm(chunks))
    return stream_llm(
        SYSTEM_PROMPT,
        f"Context:\n{context}\n\nQuestion: {query}",
    ), chunks


def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """Trả về GenerationResult."""
    chunks = retrieve(query, top_k=top_k)
    if not chunks:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": [],
            "retrieval_source": "none",
        }
    try:
        context = format_context(reorder_for_llm(chunks))
        answer = call_llm(
            SYSTEM_PROMPT,
            f"Context:\n{context}\n\nQuestion: {query}",
        )
    except Exception:
        return {
            "answer": "Tôi không thể xác minh thông tin này từ nguồn hiện có.",
            "sources": chunks,
            "retrieval_source": "none",
        }
    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": chunks[0]["retrieval_method"],
    }


if __name__ == "__main__":
    print(generate_with_citation("test query"))
