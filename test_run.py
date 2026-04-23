from collector import PaperCollector
from processor import PaperProcessor
from database import KnowledgeBase
from analyst import ResearchAnalyst
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestRun")

def test():
    logger.info("--- BẮT ĐẦU CHẠY THỬ NGHIỆM (1 BÀI BÁO) ---")
    
    collector = PaperCollector()
    processor = PaperProcessor()
    kb = KnowledgeBase()
    analyst = ResearchAnalyst()

    # 1. Tìm 1 bài báo
    logger.info("Đang tìm bài báo mới nhất...")
    papers = collector.search_papers(max_results=1)
    if not papers:
        logger.error("Không tìm thấy bài báo nào.")
        return

    paper = papers[0]
    logger.info(f"Tìm thấy: {paper['title']}")

    # 2. Tải và xử lý
    pdf_path = collector.download_pdf(paper)
    if pdf_path:
        logger.info("Đang trích xuất văn bản và phân tích bằng Ollama...")
        content = processor.extract_text_from_pdf(pdf_path)
        if content:
            analysis = processor.summarize_paper(content, paper)
            print("\n=== KẾT QUẢ PHÂN TÍCH CHI TIẾT ===")
            print(analysis)
            print("==================================\n")
            
            # 3. Lưu vào DB
            kb.add_paper(paper['id'], content, paper, analysis)
            
            # 4. Thử tạo báo cáo nhanh
            logger.info("Đang tạo thử báo cáo tổng hợp...")
            report = analyst.generate_research_report([analysis])
            print("\n=== BÁO CÁO TỔNG HỢP GỢI Ý ===")
            print(report)
            print("==============================\n")
        else:
            logger.error("Không thể trích xuất nội dung PDF.")
    else:
        logger.error("Không thể tải PDF.")

if __name__ == "__main__":
    test()
