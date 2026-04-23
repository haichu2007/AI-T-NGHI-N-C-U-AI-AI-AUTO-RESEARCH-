import ollama
from config import OLLAMA_MODEL
import logging

logger = logging.getLogger(__name__)

class ResearchAnalyst:
    def __init__(self, model=OLLAMA_MODEL):
        self.model = model

    def generate_research_report(self, analyses):
        """Analyze a collection of paper summaries to find trends and gaps."""
        combined_analyses = "\n---\n".join(analyses)
        
        prompt = f"""
        Bạn là một nhà khoa học dữ liệu và chuyên gia AI lỗi lạc. 
        Dưới đây là tóm tắt của các bài báo khoa học mới nhất mà hệ thống đã thu thập:
        
        {combined_analyses}
        
        Dựa trên các dữ liệu trên, hãy thực hiện:
        1. Tổng hợp các xu hướng nghiên cứu nổi bật nhất hiện nay trong lĩnh vực AI.
        2. Phát hiện các "khoảng trống tri thức" (knowledge gaps) hoặc các vấn đề chưa được giải quyết thỏa đáng.
        3. Đề xuất 3 hướng nghiên cứu mới, đột phá. Với mỗi hướng nghiên cứu, hãy nêu rõ:
           - Tên đề tài gợi ý.
           - Lý do tại sao hướng này quan trọng.
           - Cách tiếp cận sơ bộ.
        4. Viết một bản báo cáo tổng quan (mini-review) ngắn gọn (khoảng 500 từ).
        
        Trả lời bằng tiếng Việt, chuyên nghiệp và có tính học thuật cao.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama error during analysis: {e}")
            return "Không thể tạo báo cáo phân tích."

if __name__ == "__main__":
    analyst = ResearchAnalyst()
    # report = analyst.generate_research_report(["Summary 1...", "Summary 2..."])
    # print(report)
