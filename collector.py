import arxiv
import os
import requests
from config import PDF_DIR, ARXIV_CATEGORIES, MAX_RESULTS_PER_QUERY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperCollector:
    def __init__(self):
        self.client = arxiv.Client()

    def search_papers(self, query=None, categories=ARXIV_CATEGORIES, max_results=MAX_RESULTS_PER_QUERY):
        """Search for papers on arXiv based on categories or query."""
        if not query:
            query = " OR ".join([f"cat:{cat}" for cat in categories])
        
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        results = []
        for result in self.client.results(search):
            paper_info = {
                "id": result.entry_id.split("/")[-1],
                "title": result.title,
                "authors": [a.name for a in result.authors],
                "summary": result.summary,
                "pdf_url": result.pdf_url,
                "published": result.published,
                "categories": result.categories
            }
            results.append(paper_info)
        
        return results

    def download_pdf(self, paper_info):
        """Download the PDF of a paper."""
        file_name = f"{paper_info['id']}.pdf"
        file_path = PDF_DIR / file_name
        
        if file_path.exists():
            logger.info(f"Paper {paper_info['id']} already exists.")
            return str(file_path)

        logger.info(f"Downloading {paper_info['title']}...")
        response = requests.get(paper_info['pdf_url'])
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            return str(file_path)
        else:
            logger.error(f"Failed to download {paper_info['id']}")
            return None

if __name__ == "__main__":
    collector = PaperCollector()
    papers = collector.search_papers(max_results=2)
    for p in papers:
        collector.download_pdf(p)
