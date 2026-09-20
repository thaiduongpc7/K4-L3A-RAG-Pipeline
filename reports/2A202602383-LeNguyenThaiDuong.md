# Báo cáo cá nhân

## Thông tin

- Họ và tên: Lê Nguyễn Thái Dương
- Mã học viên: 2A202602383
- Vai trò: Trưởng nhóm
- Repository: K4-L3A-RAG-Pipeline

## Phần việc đã thực hiện

| Module/deliverable | Việc trực tiếp làm | File | Trạng thái |
|---|---|---|---|
| PageIndex fallback | Tích hợp upload PDF, cache `source -> doc_id`, kiểm tra retrieval readiness, query và chuẩn hóa kết quả | `src/task8_pageindex_vectorless.py` | Done |
| Retrieval pipeline | Nối dense search, BM25, RRF và fallback theo cosine threshold; bảo vệ lỗi provider | `src/task9_retrieval_pipeline.py` | Done |
| Generation | Reorder context, format citation, dispatch OpenAI-compatible/Gemini/Anthropic, safe refusal và streaming | `src/task10_generation.py` | Done |
| Giao diện | Xây dựng giao diện Streamlit Violet, nguồn tham khảo, chat input, màu sắc tương phản và stream token | `app.py` | Done |
| Báo cáo | Tổng hợp báo cáo nhóm và báo cáo ownership cá nhân | `GROUP_REPORT.md`, báo cáo này | Done |

## Quyết định kỹ thuật quan trọng

1. **RRF chỉ chạy một lần trong `retrieve()`.** Dense score gốc được dùng cho threshold; không dùng RRF score vì khác thang đo.
   **Trade-off:** pipeline có thêm BM25 và bước fusion nhưng tăng khả năng bắt cả paraphrase lẫn tên riêng.

2. **PageIndex được gọi theo kiểu fail-safe.** ID upload được cache; provider thiếu key, chưa ready hoặc lỗi đều không làm UI crash và hybrid result vẫn được giữ.
   **Trade-off:** fallback chỉ có kết quả khi API key và tài liệu đã sẵn sàng.

## Kiểm thử và kết quả

- `pytest tests/test_contracts.py -q`: 15 passed.
- Task 4 tạo 239 chunks từ 11 Markdown; ChromaDB dùng cosine distance.
- Dense, BM25 và hybrid retrieval đã smoke-test trên corpus thật.
- Generation không có evidence trả safe refusal; provider stream được dùng bởi Streamlit khi cấu hình hợp lệ.

## Điều còn hạn chế

- PageIndex là dịch vụ ngoài; cần `PAGEINDEX_API_KEY` và thời gian xử lý tài liệu trước khi fallback trả kết quả.
- Chất lượng câu trả lời phụ thuộc quota/model provider và chưa có bộ response cố định để đo RAGAS tự động.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh phần việc tôi trực tiếp phụ trách và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-20
- Tên thành viên: Lê Nguyễn Thái Dương
