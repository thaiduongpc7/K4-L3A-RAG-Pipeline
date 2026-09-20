# Individual contribution report

## Thông tin

- Họ và tên: Vũ Việt Hoàng
- Mã học viên: 2A202602398
- Nhóm: K4-L3A — Bước 1: Dữ liệu & Tiền xử lý (Data Engineer)
- Repository/branch: `thaiduongpc7/K4-L3A-RAG-Pipeline` — branch `main` (commit `733a988`)

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File/commit/PR | Trạng thái |
|---|---|---|---|
| Task 1 — Thu thập tài liệu chính sách | Thu thập 4 PDF quy chế/chính sách chấm thi vào `data/landing/legal/`; viết `download_documents()` kiểm tra idempotent: lọc theo đuôi `.pdf/.doc/.docx`, bỏ file ẩn, chặn file rỗng (`< 1024 bytes`), raise nếu dưới 3 tài liệu | `src/task1_collect_legal_docs.py` — commit `733a988` | Done |
| Task 2 — Crawl bài viết | Chọn và crawl các public URL về du lịch Ninh Bình; viết `ArticleParser` (`html.parser`) bóc `title/h1-h3/p/li`, loại `script/style/nav/header/footer`, khử trùng lặp và đoạn dưới 25 ký tự; lưu mỗi bài thành `article_NN.json` với 4 field bắt buộc `url / title / date_crawled / content_markdown` | `src/task2_crawl_news.py` — commit `733a988` | Done |
| Task 3 — Chuẩn hoá Markdown | Convert PDF bằng MarkItDown và JSON tin tức sang Markdown trong `data/standardized/{legal,news}/`; chèn header metadata (source, format, size, crawled date) làm dấu vết truy vết cho citation ở khâu generation | `src/task3_convert_markdown.py` — commit `733a988` | Done |
| Báo cáo cá nhân | Viết báo cáo này | `reports/2A202602398-VuVietHoang.md` | Done |

## Quyết định kỹ thuật quan trọng

1. **Quyết định:** Không dùng `crawl4ai`/Playwright như gợi ý trong template, mà crawl bằng `requests` + `HTMLParser` của thư viện chuẩn, gọi qua `asyncio.to_thread` để giữ nguyên interface `async def crawl_article(url)`.
   **Lý do/evidence:** Các trang nguồn (vnexpress, momo, mia, bestprice) đều render nội dung server-side nên không cần headless browser; bỏ được bước `playwright install` khỏi quy trình dựng môi trường của cả nhóm, chạy được trên máy không cài được browser binary.
   **Trade-off:** Mất khả năng đọc trang render bằng JavaScript. Nếu sau này nhóm thêm nguồn dạng SPA thì phải quay lại dùng crawl4ai cho riêng nguồn đó.

2. **Quyết định:** `task1` không tự tải file về mà chỉ **validate** thư mục `data/landing/legal/`; việc tải PDF làm thủ công một lần.
   **Lý do/evidence:** Nguồn PDF chính sách không có URL ổn định, và chạy lại script nhiều lần sẽ ghi đè/làm hỏng bản gốc đã thu thập. Validator đảm bảo landing zone luôn đúng số lượng và định dạng trước khi Task 3 chạy.
   **Trade-off:** Pipeline không tái tạo được dữ liệu từ zero bằng một lệnh; người chạy lại repo phải tự đặt file vào `data/landing/legal/` trước.

## Kiểm thử và kết quả

- Test/query đã dùng: chạy tuần tự `python src/task1_collect_legal_docs.py` → `task2_crawl_news.py` → `task3_convert_markdown.py`, sau đó kiểm tra số file và mở ngẫu nhiên vài file `.md` trong `data/standardized/` để xác nhận không còn rác HTML.
- Kết quả trước/sau: trước khi lọc, output chứa nhiều dòng menu/footer lặp lại giữa các bài cùng site; sau khi thêm blacklist thẻ + khử trùng lặp + ngưỡng 25 ký tự, nội dung còn lại chủ yếu là phần thân bài.
- Lỗi đã phát hiện và cách xử lý:
  - Một số URL trả về trang gần như rỗng (chặn bot/redirect) → thêm guard `len(markdown) < 200` raise `ValueError`, và `crawl_all()` bắt exception theo từng URL để một bài lỗi không làm hỏng cả batch.
  - PDF scan không bóc được text → `convert_legal_docs()` raise khi `text_content` rỗng thay vì ghi file Markdown trống làm hỏng index ở Task 4.
  - Thiếu field metadata trong JSON → `convert_news_articles()` kiểm tra đủ 4 key trước khi ghi.

## Điều còn hạn chế

- Hạn chế cụ thể: bộ lọc nội dung là heuristic chung (theo thẻ + độ dài), chưa nhắm vào vùng article của từng site, nên vẫn lọt một ít đoạn quảng cáo/"bài liên quan" vào corpus; `task1` cũng chưa kiểm tra trùng nội dung giữa các PDF.
- Nếu có thêm thời gian: thay heuristic bằng trafilatura (hoặc selector riêng cho mỗi domain) để bóc đúng phần thân bài, và thêm hash nội dung để phát hiện trùng lặp ngay tại landing zone — giúp precision ở khâu retrieval của các bạn sau tăng lên.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 20/09/2026
- Tên thành viên: Vũ Việt Hoàng
