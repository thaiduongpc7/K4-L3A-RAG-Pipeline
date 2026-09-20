# Báo cáo tổng kết đồ án

## 1. Tổng quan

Nhóm xây dựng Violet, một chatbot RAG hỗ trợ khám phá thông tin du lịch và chính sách liên quan đến Ninh Bình. Pipeline gồm thu thập dữ liệu, chuẩn hóa Markdown, chunking, embedding, ChromaDB, dense search, BM25, RRF, PageIndex fallback và generation có citation.

## 2. Kiến trúc và dữ liệu

- `data/landing/`: giữ PDF và JSON gốc để truy vết khi convert sai.
- `data/standardized/`: nguồn duy nhất của Task 4, gồm `legal/` và `news/`; thư mục giữ `doc_type` xuyên suốt pipeline.
- Task 4 dùng chunk `500` ký tự, overlap `50`, ID ổn định và embedding `sentence-transformers/all-MiniLM-L6-v2`.
- ChromaDB persistent dùng cosine distance; BM25 dùng đúng corpus chunks của Task 4.

## 3. Retrieval và fallback

Dense search bắt ý nghĩa gần đúng, BM25 bắt từ khóa/tên riêng. Task 7 hợp nhất bằng RRF một lần với công thức `sum(1 / (k + rank))`, rank bắt đầu từ 1. Task 9 so threshold bằng cosine score gốc của dense. Khi điểm thấp, PageIndex được gọi trong `try/except`; lỗi provider không làm UI crash và hybrid result được giữ lại.

## 4. Generation và giao diện

Task 10 reorder context để giảm lost-in-the-middle, format `[Document X | Title | Source]`, dispatch provider theo `.env`, và safe refusal khi thiếu evidence hoặc provider lỗi. Streamlit Violet cung cấp chat interface, nguồn tham khảo, control top-k, giao diện responsive, màu tương phản và stream token cho OpenAI-compatible/Gemini khi provider được cấu hình.

## 5. Kiểm thử

- Contract suite: `15 passed`.
- Acceptance Task 1-3: `3 passed`.
- Corpus thật: 3 PDF legal, 8 JSON news, 11 Markdown, 239 chunks.
- ChromaDB smoke test: collection metric `cosine`, dense và BM25 trả kết quả giảm dần.
- Safe refusal đã được kiểm tra khi không có evidence hoặc thiếu cấu hình LLM.

## 6. Hạn chế và hướng phát triển

PageIndex cần API key và thời gian xử lý tài liệu từ dịch vụ ngoài. Các metric generation như faithfulness và answer relevance cần một evaluation runner có response cố định để đo tái lập. Bước tiếp theo là calibrate threshold bằng query in-domain/out-of-domain, lưu trace retrieval và bổ sung policy extraction cho các PDF có lớp text hạn chế.
