from collector import PaperCollector
from processor import PaperProcessor
from database import KnowledgeBase
from analyst import ResearchAnalyst
import logging
import os
import sys

# Set encoding for console output if possible
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestRun")

def test():
    logger.info("--- START TEST RUN (1 PAPER) ---")
    
    collector = PaperCollector()
    
    # Check for available models
    import ollama
    try:
        models_resp = ollama.list()
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
                logger.info("Using tinyllama for speed.")
    except Exception as e:
        logger.error(f"Error checking models: {e}")
        model_to_use = "llama3"

    processor = PaperProcessor(model=model_to_use)
    kb = KnowledgeBase()
    analyst = ResearchAnalyst(model=model_to_use)

    # 1. Search
    logger.info("Searching for latest paper...")
    papers = collector.search_papers(max_results=1)
    if not papers:
        logger.error("No papers found.")
        return

    paper = papers[0]
    logger.info(f"Found: {paper['title']}")

    # 2. Process
    pdf_path = collector.download_pdf(paper)
    if pdf_path:
        logger.info("Extracting text and analyzing with Ollama...")
        content = processor.extract_text_from_pdf(pdf_path)
        if content:
            analysis = processor.summarize_paper(content, paper)
            
            # Save to file to avoid console encoding issues
            result_file = "test_result.md"
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(f"# KẾT QUẢ CHẠY THỬ AI\n\n")
                f.write(f"## Bài báo: {paper['title']}\n\n")
                f.write(f"### Phân tích từ {model_to_use}:\n\n")
                f.write(analysis)
                f.write("\n\n---\n\n")
                
                # 3. Store in DB
                kb.add_paper(paper['id'], content, paper, analysis)
                
                # 4. Generate suggestion
                logger.info("Generating research suggestion...")
                report = analyst.generate_research_report([analysis])
                f.write(f"### Gợi ý hướng nghiên cứu:\n\n")
                f.write(report)

            logger.info(f"SUCCESS! Results saved to {result_file}")
            print(f"DONE. Check {result_file} for details.")
        else:
            logger.error("Failed to extract content.")
    else:
        logger.error("Failed to download PDF.")

if __name__ == "__main__":
    test()
