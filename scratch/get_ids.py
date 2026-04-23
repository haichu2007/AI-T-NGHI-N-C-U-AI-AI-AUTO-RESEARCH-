import chromadb
from pathlib import Path

BASE_DIR = Path("c:/Users/Administrator/Downloads/AI TỰ NGHIÊN CỨU AI (AI AUTO RESEARCH)")
DB_DIR = BASE_DIR / "data" / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(name="ai_research")
results = collection.get()
print(results['ids'])
