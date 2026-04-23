import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
DB_DIR = DATA_DIR / "chroma_db"
LOG_FILE = DATA_DIR / "research_system.log"

# Ensure directories exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)

# Ollama Configuration
OLLAMA_MODEL = "llama3"  # or mistral, mixtral, etc.
OLLAMA_EMBED_MODEL = "nomic-embed-text" # Model for generating embeddings

# ArXiv Configuration
ARXIV_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL", "cs.CV"]
MAX_RESULTS_PER_QUERY = 5

# Research Configuration
UPDATE_INTERVAL_DAYS = 1
IDEATION_INTERVAL_DAYS = 7
