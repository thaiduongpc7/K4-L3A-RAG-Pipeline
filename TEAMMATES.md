# Phân công thành viên nhóm

## 🟦 BƯỚC 1: Dữ liệu & Tiền xử lý

**Vũ Việt Hoàng — 2A202602398**

> Data Engineer: phụ trách đầu vào của toàn bộ hệ thống.

- `src/task1_collect_legal_docs.py`: Tải tài liệu PDF và lưu vào `data/landing/legal/`.
- `src/task2_crawl_news.py`: Cào bài viết từ web và lưu vào `data/landing/news/`.
- `src/task3_convert_markdown.py`: Chuyển PDF và JSON thành Markdown chuẩn trong `data/standardized/`.
- `2A202602398-VuVietHoang.md`: Báo cáo cá nhân Data Engineer.

## 🟩 BƯỚC 2: Phân đoạn, Embedding & Vector DB

**Nguyễn Văn Quốc Việt — 2A202602973**

> Vector DB Engineer: nhận Markdown từ Bước 1 để xây dựng cơ sở dữ liệu vector.

- `src/task4_chunking_indexing.py`: Chia Markdown thành chunks, embedding và nạp vào persistent collection `chroma_db/`.
- `src/task5_semantic_search.py`: Tìm kiếm ngữ nghĩa Dense Search bằng khoảng cách cosine trên ChromaDB.
- `2A202602973-NguyenVanQuocViet.md`: Báo cáo cá nhân Vector DB.

## 🟧 BƯỚC 3: Tìm kiếm từ khóa, Xếp hạng & Đánh giá

**Nguyễn Phát Thịnh — 2A202602645**

> Evaluation Specialist: phụ trách tìm kiếm từ khóa, xếp hạng và thực nghiệm A/B Testing.

- `src/task6_lexical_search.py`: Tìm kiếm từ khóa chính xác bằng BM25Okapi và cache bộ nhớ.
- `src/task7_reranking.py`: Dung hợp thứ hạng bằng Reciprocal Rank Fusion (RRF, `k = 60`).
- `group_project/evaluation/golden_dataset.json`: Bộ dữ liệu vàng gồm các câu hỏi, đáp án và context tiếng Việt.
- `group_project/evaluation/RESULT.md`: Báo cáo đánh giá các chỉ số và so sánh A/B.
- `2A202602645-NguyenPhatThinh.md`: Báo cáo cá nhân Evaluation Specialist.

## 🟪 BƯỚC 4: Tích hợp Pipeline, Sinh câu trả lời & Giao diện Web

**Lê Nguyễn Thái Dương — 2A202602383**

> Trưởng nhóm: kết nối toàn bộ pipeline, điều khiển LLM sinh câu trả lời và xây dựng giao diện người dùng cuối.

- `src/task8_pageindex_vectorless.py`: Cơ chế PageIndex Fallback khi cosine score thấp.
- `src/task9_retrieval_pipeline.py`: Kết nối Dense Search, Lexical Search, RRF và Fallback Check.
- `src/task10_generation.py`: Anti lost-in-the-middle, citation `[Document X]`, Gemini/LLM dispatch và Safe Refusal.
- `app.py`: Giao diện Web Streamlit, chat input, source display và stream token.
- `GROUP_REPORT.md`: Báo cáo tổng kết đồ án toàn nhóm.
- `2A202602383-LeNguyenThaiDuong.md`: Báo cáo cá nhân Leader.
