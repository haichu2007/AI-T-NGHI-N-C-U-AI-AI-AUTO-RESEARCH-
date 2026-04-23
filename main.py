import schedule
import time
import logging
from datetime import datetime
from collector import PaperCollector
from processor import PaperProcessor
from database import KnowledgeBase
from analyst import ResearchAnalyst
from config import LOG_FILE, DATA_DIR

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AI_Researcher")

def run_research_cycle():
    logger.info("Starting a new research cycle...")
    
    collector = PaperCollector()
    processor = PaperProcessor()
    kb = KnowledgeBase()
    analyst = ResearchAnalyst()

    # 1. Collect
    logger.info("Searching for new papers on arXiv...")
    papers = collector.search_papers(max_results=5) # Adjust limit as needed
    
    for paper in papers:
        paper_id = paper['id']
        # Check if already processed (exists in KB)
        try:
            existing = kb.collection.get(ids=[paper_id])
            if existing and existing['ids']:
                logger.info(f"Paper {paper_id} already in database. Skipping.")
                continue
        except:
            pass

        # 2. Download and Process
        pdf_path = collector.download_pdf(paper)
        if pdf_path:
            logger.info(f"Extracting text and analyzing {paper['title']}...")
            content = processor.extract_text_from_pdf(pdf_path)
            if content:
                analysis = processor.summarize_paper(content, paper)
                
                # 3. Store
                kb.add_paper(paper_id, content, paper, analysis)
                logger.info(f"Successfully processed {paper_id}")
            else:
                logger.warning(f"No content extracted from {paper_id}")

    # 4. Generate Global Report
    logger.info("Generating global research report...")
    all_analyses = kb.get_all_analyses()
    if all_analyses:
        report = analyst.generate_research_report(all_analyses)
        
        report_path = DATA_DIR / f"report_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Global research report generated at {report_path}")
    else:
        logger.warning("No analyses found to generate report.")

    logger.info("Research cycle completed.")

def main():
    logger.info("AI Auto Research System is running...")
    
    # Run once at startup
    run_research_cycle()

    # Schedule: Run every day at 00:00
    schedule.every().day.at("00:00").do(run_research_cycle)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
