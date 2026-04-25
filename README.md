# Local Ollama Word + Excel UI

Ứng dụng này sử dụng model `deepseek` đã cài sẵn trong Ollama để tạo nội dung và ghi ra file Word/Excel trên máy tính Windows.

## Yêu cầu

- Ollama đã được cài và model `deepseek` đã sẵn sàng.
- Ollama API local thường chạy ở `http://127.0.0.1:11434`.
- Python 3.10+ (đã có sẵn `.venv` trong workspace).

## Cài đặt

1. Kích hoạt virtual environment:

```powershell
cd "c:\Users\Administrator\Downloads\AI-T-NGHI-N-C-U-AI-AI-AUTO-RESEARCH-"
.\.venv\Scripts\Activate.ps1
```

2. Cài thư viện:

```powershell
pip install -r requirements.txt
```

## Chạy ứng dụng

```powershell
python main.py
```

## Sử dụng

1. Chọn loại file `Word` hoặc `Excel`.
2. Chọn đường dẫn lưu file.
3. Nhập prompt / yêu cầu cho Ollama.
4. Nhấn `Chạy và lưu kết quả` để tạo nội dung và lưu vào Word/Excel.
5. Nếu muốn tạo file Excel trống trước, chọn `Excel`, chọn đường dẫn và nhấn `Tạo file Excel`.

Ứng dụng sẽ gửi prompt đến Ollama local, lấy kết quả trả về và lưu thành file Word hoặc Excel. Bạn cũng có thể tạo file Excel trống bằng nút `Tạo file Excel`.

## Lưu ý

- Nếu Ollama không đang chạy, vui lòng bật server Ollama hoặc dùng lệnh phù hợp với cài đặt của bạn.
- Ứng dụng hiện tại tạo thêm nội dung mới vào file nếu file đã tồn tại.
