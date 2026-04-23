# Hệ thống AI Tự Động Nghiên Cứu về AI (Ollama-based)

Hệ thống này được thiết kế để tự động hóa quá trình nghiên cứu khoa học trong lĩnh vực Trí tuệ nhân tạo. Hệ thống tự động quét arXiv, tải tài liệu, phân tích nội dung bằng các mô hình ngôn ngữ lớn (LLM) chạy cục bộ qua Ollama, và đề xuất các hướng nghiên cứu mới.

## Kiến trúc hệ thống
1. **Collector**: Tìm kiếm và tải các bài báo mới nhất từ arXiv.
2. **Processor**: Trích xuất văn bản từ PDF và sử dụng Ollama để tóm tắt/phân tích chuyên sâu.
3. **Knowledge Base**: Lưu trữ dữ liệu và vector embedding vào ChromaDB để truy xuất thông tin hiệu quả.
4. **Analyst**: Tổng hợp tri thức từ kho dữ liệu để phát hiện xu hướng và sinh ý tưởng nghiên cứu.
5. **Scheduler**: Lập lịch chạy tự động hàng ngày.

## Yêu cầu hệ thống
- Python 3.10+
- [Ollama](https://ollama.com/) đã được cài đặt và đang chạy.
- Các mô hình Ollama cần thiết:
  - `llama3` (cho phân tích và tóm tắt)
  - `nomic-embed-text` (cho tạo vector embedding)

Cài đặt mô hình:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

## Hướng dẫn cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

2. Cấu hình (nếu cần):
Chỉnh sửa file `config.py` để thay đổi mô hình, danh mục arXiv hoặc tần suất cập nhật.

## Cách chạy hệ thống

Chạy chương trình chính:
```bash
python main.py
```

Khi chạy, hệ thống sẽ:
1. Quét arXiv tìm các bài báo mới nhất.
2. Tải PDF về thư mục `data/pdfs/`.
3. Phân tích nội dung và lưu vào cơ sở dữ liệu `data/chroma_db/`.
4. Xuất một bản báo cáo định kỳ dưới dạng Markdown trong thư mục `data/`.

## Cấu trúc thư mục
- `collector.py`: Module thu thập dữ liệu.
- `processor.py`: Module xử lý PDF và LLM prompt.
- `database.py`: Quản lý kho tri thức vector.
- `analyst.py`: Phân tích xu hướng và sinh ý tưởng.
- `main.py`: Điều phối và lập lịch.
- `data/`: Nơi lưu trữ PDF, database và báo cáo.

## Lưu ý
- Đảm bảo Ollama server đang chạy (`ollama serve`) trước khi khởi động hệ thống.
- Hệ thống tóm tắt khoảng 8000 ký tự đầu tiên của bài báo để tối ưu hóa context window của mô hình.
