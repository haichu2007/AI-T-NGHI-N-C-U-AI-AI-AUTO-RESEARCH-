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

    def refine_and_upgrade_topic(self, seed_topic, findings):
        """AI Agent 2: Architect/Critic. Refines the topic based on findings and upgrades it."""
        combined_findings = "\n---\n".join(findings)
        
        prompt = f"""
        Bạn là một Kiến trúc sư AI cấp cao (Senior AI Architect).
        Chủ đề nghiên cứu ban đầu: {seed_topic}
        
        Dưới đây là các kết quả nghiên cứu mới nhất mà AI 1 đã tìm được:
        {combined_findings}
        
        Nhiệm vụ của bạn:
        1. Đánh giá xem chủ đề ban đầu có còn phù hợp với xu hướng hiện tại không?
        2. Tinh chỉnh (Refine) chủ đề ban đầu để trở nên chuyên sâu và đột phá hơn.
        3. Đề xuất một "Bản nâng cấp" (Upgrade) cho hướng nghiên cứu này (A11 Level).
        4. Tạo ra một "Từ khóa tìm kiếm mới" (New Search Query) để AI 1 tiếp tục tìm kiếm sâu hơn.
        
        Trả lời bằng tiếng Việt, phân tích sắc sảo và mang tính định hướng tương lai.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception as e:
            logger.error(f"Architect Agent error: {e}")
            return "Không thể tinh chỉnh chủ đề."

if __name__ == "__main__":
    analyst = ResearchAnalyst()
    # report = analyst.generate_research_report(["Summary 1...", "Summary 2..."])
    # print(report)
