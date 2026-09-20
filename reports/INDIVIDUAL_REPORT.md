# Báo cáo đóng góp cá nhân

## Thông tin

- Họ và tên: Lê Nguyễn Thái Dương
- Mã học viên: 2A202602383
- Vai trò: Trưởng nhóm
- Repository: K4-L3A-RAG-Pipeline

## Phần việc đã thực hiện

| Module/deliverable | Việc trực tiếp làm | File/đầu ra đối chiếu | Trạng thái |
|---|---|---|---|
| PageIndex fallback | Tích hợp upload PDF, cache `source -> doc_id`, kiểm tra readiness, query và chuẩn hóa kết quả | [src/task8_pageindex_vectorless.py](../src/task8_pageindex_vectorless.py) | Done |
| Retrieval pipeline | Nối dense search, BM25, RRF và fallback theo cosine threshold; bảo vệ lỗi provider | [src/task9_retrieval_pipeline.py](../src/task9_retrieval_pipeline.py) | Done |
| Generation | Reorder context, format citation, dispatch provider và safe refusal | [src/task10_generation.py](../src/task10_generation.py) | Done |
| Giao diện người dùng | Xây dựng Streamlit UI, chat input, nguồn tham khảo, màu tương phản và streaming | [app.py](../app.py) | Done |
| Báo cáo nhóm | Tổng hợp kiến trúc, kiểm thử, hạn chế và hướng phát triển | [GROUP_REPORT.md](../GROUP_REPORT.md) | Done |

## Quyết định kỹ thuật quan trọng

1. **Dùng cosine score gốc của dense search cho fallback.** RRF chỉ được gọi một lần để hợp nhất dense và BM25; không dùng RRF score để so threshold vì hai thang đo khác nhau.
   **Evidence:** `retrieve()` lấy `dense[0]["score"]` trước khi gọi PageIndex; contract test kiểm tra fallback và số lần gọi RRF.
   **Trade-off:** Cần chạy thêm BM25 và RRF, nhưng kết quả bắt được cả truy vấn diễn đạt gần nghĩa và tên riêng chính xác.

2. **PageIndex được triển khai theo kiểu fail-safe.** Document ID được cache; khi thiếu API key, tài liệu chưa sẵn sàng hoặc provider lỗi, pipeline giữ hybrid result hoặc trả safe refusal thay vì làm UI crash.
   **Evidence:** `pageindex_search()` trả danh sách rỗng khi chưa cấu hình; `retrieve()` bọc fallback trong `try/except`.
   **Trade-off:** Fallback phụ thuộc dịch vụ ngoài và không hoạt động đầy đủ nếu chưa có `PAGEINDEX_API_KEY`.

## Kiểm thử và kết quả

- `pytest tests/test_contracts.py -q`: **15 passed**.
- Acceptance Task 1-3: **3 passed** cho legal documents, news metadata và standardized Markdown.
- Task 4 tạo 239 chunks từ 11 Markdown; ChromaDB dùng cosine distance.
- Dense, BM25 và hybrid retrieval đã được smoke-test trên corpus thật.
- Generation không có evidence trả safe refusal; giao diện hỗ trợ streaming khi provider được cấu hình.

## Điều còn hạn chế

- PageIndex cần API key và thời gian xử lý tài liệu từ dịch vụ ngoài; chưa thể đo fallback live trong môi trường không có key.
- Các metric generation như faithfulness và answer relevance chưa có response set cố định để tái lập tự động.
- Hai PDF policy có lớp text hạn chế, nên cần re-extract hoặc OCR để tăng context recall.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh phần việc mình trực tiếp phụ trách và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-20
- Tên thành viên: Lê Nguyễn Thái Dương
