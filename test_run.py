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
    
    # Check for available models
    import ollama
    try:
        models_resp = ollama.list()
        # Handle both object and dict return types
        models = models_resp.models if hasattr(models_resp, 'models') else models_resp.get('models', [])
        available_names = []
        for m in models:
            if hasattr(m, 'model'): available_names.append(m.model)
            elif isinstance(m, dict): available_names.append(m.get('name', ''))
        
        logger.info(f"Models found: {available_names}")
        model_to_use = "llama3"
        if not any("llama3" in name for name in available_names):
            if any("tinyllama" in name for name in available_names):
                model_to_use = "tinyllama"
                logger.info("Using tinyllama for fast test.")
            else:
                logger.warning("llama3 not found, trying default.")
    except Exception as e:
        logger.error(f"Error checking models: {e}")
        model_to_use = "llama3" # Fallback to default

    processor = PaperProcessor(model=model_to_use)
    kb = KnowledgeBase()
    analyst = ResearchAnalyst(model=model_to_use)

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
