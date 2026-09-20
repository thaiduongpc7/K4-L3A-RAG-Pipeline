# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Văn Quốc Việt
- Mã học viên: 2A202602973
- Nhóm: Violet
- Repository/branch: https://github.com/thaiduongpc7/K4-L3A-RAG-Pipeline — branch `viet/task4-5`
- Phần được phân công: **Task 4 (chunking, embedding, indexing) và Task 5 (semantic search)**

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 4 — Chunking & indexing | `embed_texts()` (dispatch theo `EMBEDDING_PROVIDER`, lazy-load + cache model, `normalize_embeddings=True`); `get_collection()` (Chroma persistent client, `hnsw:space="cosine"`); `load_documents()` (quét `data/standardized/**/*.md`, suy `doc_type` từ thư mục cấp một, lấy `title` từ dòng `# `, lấy `url` từ dòng `**Source:**`); `chunk_documents()` (`RecursiveCharacterTextSplitter` 500/50, id `<path>::chunk-<index>`, bỏ chunk rỗng); `embed_chunks()` (kiểm tra số vector khớp số chunk); `index_to_vectorstore()` (`upsert` theo id ổn định) | [src/task4_chunking_indexing.py](../src/task4_chunking_indexing.py) — commit `56feb41` | Done |
| Task 5 — Semantic search | `semantic_search()`: dùng lại `embed_texts()` + `get_collection()` của Task 4 (một embedding provider duy nhất cho cả index và query), query Chroma, đổi cosine distance sang score `max(0.0, 1.0 - distance)`, gắn `retrieval_method="dense"`, guard `top_k <= 0` và query rỗng, sort giảm dần rồi cắt `top_k` | [src/task5_semantic_search.py](../src/task5_semantic_search.py) — commit `56feb41` | Done |
| Build chỉ mục thật (`chroma_db/`) | Chưa chạy được end-to-end: máy tôi chưa cài `chromadb` và `sentence-transformers`, thư mục `chroma_db/` chưa tồn tại | — | Partial |

Ngoài hai module trên tôi không nhận phần khác; Task 1–3 và 6–10 hiện vẫn ở trạng thái `NotImplementedError` và thuộc các thành viên khác.

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Đổi embedding model mặc định từ `BAAI/bge-m3` (1024 chiều) sang `sentence-transformers/all-MiniLM-L6-v2` (384 chiều), cho override qua biến `EMBEDDING_MODEL` trong `.env`, và sửa `EMBEDDING_DIM = 384` cho khớp.
   **Lý do/evidence:** bge-m3 nặng (>2 GB, chạy CPU rất chậm) nên cả nhóm không kịp build lại chỉ mục trong thời lượng lab. MiniLM tải nhanh, chạy được trên CPU, đủ để dựng và kiểm thử toàn bộ đường đi dữ liệu Task 4 → Task 5.
   **Trade-off:** MiniLM chủ yếu huấn luyện tiếng Anh, trong khi corpus nhóm là văn bản pháp quy và tin tức tiếng Việt, nên chất lượng dense retrieval sẽ kém hơn bge-m3. Đây là đánh đổi lấy tốc độ; cần đổi lại model đa ngữ trước khi chạy A/B chính thức trong `evaluation/RESULT.md`.

2. **Quyết định:** Dùng chunk id dạng `<đường-dẫn-tương-đối>::chunk-<index>` và gọi `upsert()` thay vì `add()`.
   **Lý do/evidence:** `docs/MODULE_CONTRACTS.md` yêu cầu id duy nhất và ổn định, chạy index lại không được sinh dữ liệu trùng. Id sinh từ đường dẫn file nên bất biến giữa các lần chạy; `upsert` ghi đè đúng bản ghi cũ. Kiểm chứng trên corpus thật: 239 chunk / 239 id duy nhất.
   **Trade-off:** Nếu nội dung một file bị rút ngắn làm số chunk giảm, các chunk cũ có `chunk_index` lớn hơn vẫn nằm lại trong collection vì `upsert` không xoá. Muốn sạch tuyệt đối phải `delete(where={"source": ...})` trước khi index lại.

## Kiểm thử và kết quả

- **Test đã chạy:** `pytest tests/test_contracts.py -q`. Ba test phủ trực tiếp phần tôi làm đều PASSED:
  - `test_public_function_signatures_are_stable`
  - `test_chunk_documents_preserves_identity_and_metadata`
  - `test_semantic_search_uses_shared_embedding_and_contract` (monkeypatch `embed_texts` + `get_collection`, kiểm tra query dùng chung hàm embed của Task 4 và output đúng `SearchResult`)

  Toàn file hiện là **9 passed, 6 failed**; cả 6 failed đều là `NotImplementedError` của Task 6–10 (`lexical_search`, `rerank_rrf`, `reorder_for_llm`, `retrieve`), không thuộc phần tôi phụ trách.
- **Chạy trên dữ liệu thật (không cần Chroma):** `load_documents()` đọc được **11 tài liệu** (3 legal, 8 news), 8 tài liệu lấy được `url` từ dòng `**Source:**`. `chunk_documents()` sinh **239 chunk**, 239 id duy nhất, độ dài trung bình 368 ký tự, dài nhất 499 ký tự — nằm trong `CHUNK_SIZE = 500` mà test kiểm tra.
- **Trước/sau:** trước khi tôi làm, `chunk_documents` và `semantic_search` raise `NotImplementedError` và hai test tương ứng FAILED; sau khi hiện thực, cả hai chuyển sang PASSED.
- **Môi trường:** để chạy được test chunking phải cài thêm `langchain-text-splitters` vào venv (thiếu package này test báo `ModuleNotFoundError`, không phải lỗi code).
- **Lỗi đã phát hiện và cách xử lý:**
  - `load_documents()` theo gợi ý ban đầu suy `doc_type` bằng `"legal" in path.parts`; cách này nhận nhầm khi tên file chứa chữ "legal". Đổi sang `relative_path.parts[0]` và bỏ qua thư mục ngoài `{legal, news}`.
  - Splitter có thể trả mảnh chỉ gồm khoảng trắng, vi phạm yêu cầu chunk không rỗng → lọc `if text.strip()`.
  - `embed_chunks()` sẽ âm thầm bỏ sót chunk nếu số vector trả về ít hơn số chunk (do `zip` cắt ngắn) → thêm kiểm tra độ dài và raise `ValueError`.
  - Chroma trả cosine distance có thể > 1 với vector đã normalize ở biên số học, làm score âm → kẹp bằng `max(0.0, 1.0 - distance)` để giữ `score >= 0` như contract.

## Điều còn hạn chế

- Hạn chế cụ thể: tôi mới kiểm chứng chunking trên dữ liệu thật và kiểm chứng hợp đồng của `semantic_search` bằng test có monkeypatch; **chưa build `chroma_db/` và chưa đo chất lượng retrieval thật** trên corpus tiếng Việt, nên chưa thể khẳng định MiniLM 384 chiều đủ dùng cho dữ liệu nhóm.
- Nếu có thêm thời gian, việc đầu tiên: cài `chromadb` + `sentence-transformers`, chạy `python -m src.task4_chunking_indexing` để index 239 chunk, rồi A/B `all-MiniLM-L6-v2` với một model đa ngữ (`BAAI/bge-m3` hoặc `paraphrase-multilingual-MiniLM-L12-v2`) trên golden dataset, lấy số đo đó làm căn cứ chọn model chính thức thay vì chọn theo tốc độ.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-20
- Tên thành viên: Nguyễn Văn Quốc Việt
