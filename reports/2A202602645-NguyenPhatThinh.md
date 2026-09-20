# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Phát Thịnh
- Mã học viên: 2A202602645
- Nhóm: K4-L3A-RAG-Pipeline
- Repository/branch: PhatThinh_2A202602645

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Bổ trợ tìm kiếm | Tìm kiếm từ khóa chính xác BM25Okapi kèm cache bộ nhớ | `src/task6_lexical_search.py` | Done |
| Bổ trợ tìm kiếm | Thuật toán dung hợp thứ hạng RRF (k = 60) | `src/task7_reranking.py` | Done |
| Evaluation | Bộ dữ liệu vàng gồm 16 câu hỏi – đáp có context chuẩn | `group_project/evaluation/golden_dataset.json` | Done |
| Evaluation | Báo cáo đánh giá 4 chỉ số và so sánh A/B | `reports/RESULT.md` | Partial (Chờ Pipeline) |

## Quyết định kỹ thuật quan trọng

Mô tả tối đa hai quyết định mà bạn trực tiếp tham gia:

1. **Quyết định:** Thêm biến global caching `_BM25_INDEX` để lưu trữ object model của BM25.
   **Lý do/evidence:** Việc rebuild lại model BM25Okapi mỗi khi query tốn quá nhiều tài nguyên xử lý và làm tăng latency của toàn bộ pipeline tìm kiếm. BM25 model phụ thuộc vào corpus tĩnh nên có thể cache an toàn.
   **Trade-off:** Sẽ tốn thêm một ít RAM bộ nhớ để duy trì model BM25 thường trực, bù lại tốc độ search đạt mức mili-giây.

2. **Quyết định:** Lựa chọn `k = 60` cho thuật toán Reciprocal Rank Fusion (RRF).
   **Lý do/evidence:** RRF với hằng số phạt k=60 là giá trị tiêu chuẩn và được thực nghiệm chứng minh là mang lại sự ổn định cao khi dung hợp Dense và Sparse retrieval.
   **Trade-off:** Giá trị này khiến rank thấp (vd rank 5, rank 6) không quá khác biệt về score, do đó RRF chỉ thực sự hữu ích để re-order chứ không dùng để quyết định fallback.

## Kiểm thử và kết quả

- Test hoặc query tôi đã dùng: `pytest tests/test_contracts.py::test_lexical_search_returns_bm25_contract` và `pytest tests/test_contracts.py::test_task7_reranking`
- Kết quả trước/sau nếu có: Xử lý thành công lỗi rebuild BM25 mỗi query, giảm độ trễ truy vấn rõ rệt.
- Lỗi đã phát hiện và cách xử lý: Lỗi `ModuleNotFoundError: No module named 'rank_bm25'` trên máy local do thiếu package, xử lý bằng cách activate lại môi trường ảo `.venv` và cài lại các dependency từ pyproject.toml.

## Điều còn hạn chế

- Một hạn chế cụ thể của phần tôi làm: Phần kết quả đánh giá (RESULT.md) vẫn đang tạm ở mức "Not measured" do hệ thống Dense Search và Generation của nhóm chưa hoàn thiện. Chưa thể lấy được score so sánh A/B thực tế.
- Nếu có thêm thời gian, thay đổi đầu tiên tôi sẽ thực hiện: Chạy Ragas end-to-end trên 16 câu hỏi vàng để lấy số đo chính xác về Faithfulness, Relevance, Recall, Precision bổ sung vào báo cáo.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Nguyễn Phát Thịnh
