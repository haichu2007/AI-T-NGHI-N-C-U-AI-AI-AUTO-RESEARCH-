import ollama
from pdfminer.high_level import extract_text
import logging
from config import OLLAMA_MODEL, OLLAMA_OPTIONS

logger = logging.getLogger(__name__)

class PaperProcessor:
    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from a PDF file."""
        try:
            text = extract_text(pdf_path)
            return text
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""

    def summarize_paper(self, text, metadata):
        """Summarize the paper and extract key insights using Ollama."""
        # Truncate text if too long for the model context window (heuristic)
        context_text = text[:8000] 
        
        prompt = f"""
        Bạn là một trợ lý nghiên cứu AI chuyên sâu. Hãy phân tích bài báo sau:
        Tiêu đề: {metadata['title']}
        Tóm tắt gốc: {metadata['summary']}
        
        Nội dung chi tiết (một phần):
        {context_text}
        
        Yêu cầu:
        1. Tóm tắt các đóng góp chính của bài báo (3-5 câu).
        2. Đánh giá mức độ mới và ảnh hưởng đến lĩnh vực AI hiện nay.
        3. Liệt kê các phương pháp chính được sử dụng.
        4. Xác định các hạn chế và các hướng nghiên cứu mở mà tác giả đề cập.
        5. Đưa ra 1 ý tưởng nghiên cứu kế thừa từ bài báo này.
        
        Trả lời bằng tiếng Việt, súc tích và chuyên sâu.
        """
        
        try:
            response = ollama.chat(
                model=self.model, 
                messages=[{'role': 'user', 'content': prompt}],
                options=OLLAMA_OPTIONS
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return "Không thể tóm tắt bài báo."

if __name__ == "__main__":
    # Example usage (requires Ollama running)
    processor = PaperProcessor()
    # test_text = "This is a test content of an AI paper..."
    # summary = processor.summarize_paper(test_text, {"title": "Test Paper", "summary": "Test summary"})
    # print(summary)
