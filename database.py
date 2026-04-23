import chromadb
from chromadb.utils import embedding_functions
import ollama
from config import DB_DIR, OLLAMA_EMBED_MODEL
import logging

logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, collection_name="ai_research"):
        self.client = chromadb.PersistentClient(path=str(DB_DIR))
        # Custom embedding function using Ollama
        self.embed_fn = embedding_functions.OllamaEmbeddingFunction(
            model_name=OLLAMA_EMBED_MODEL,
            url="http://localhost:11434/api/embeddings",
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embed_fn
        )

    def add_paper(self, paper_id, content, metadata, analysis):
        """Add a paper to the vector database."""
        # We store the analysis as part of metadata or a separate document
        self.collection.add(
            ids=[paper_id],
            documents=[content[:5000]], # Store a chunk of content for retrieval
            metadatas=[{
                "title": metadata["title"],
                "authors": ", ".join(metadata["authors"]),
                "analysis": analysis,
                "url": metadata["pdf_url"]
            }]
        )
        logger.info(f"Added paper {paper_id} to knowledge base.")

    def search_similar(self, query, n_results=3):
        """Search for papers similar to a query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results

    def get_all_analyses(self):
        """Retrieve all stored analyses for global trend analysis."""
        results = self.collection.get()
        return [m["analysis"] for m in results["metadatas"]]

class UserMemory:
    def __init__(self, collection_name="user_memory"):
        self.client = chromadb.PersistentClient(path=str(DB_DIR))
        self.embed_fn = embedding_functions.OllamaEmbeddingFunction(
            model_name=OLLAMA_EMBED_MODEL,
            url="http://localhost:11434/api/embeddings",
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embed_fn
        )

    def add_memory(self, content):
        """Store a fact or piece of information about the user/context."""
        import uuid
        memory_id = str(uuid.uuid4())
        self.collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[{"timestamp": str(datetime.now())}]
        )
        logger.info(f"Added new memory: {content}")

    def get_relevant_memories(self, query, n_results=5):
        """Retrieve relevant memories based on the query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []

    def get_all_memories(self):
        """Return all stored memories."""
        results = self.collection.get()
        return results["documents"] if results["documents"] else []

    def clear_memory(self):
        """Wipe all memories."""
        ids = self.collection.get()["ids"]
        if ids:
            self.collection.delete(ids=ids)

if __name__ == "__main__":
    kb = KnowledgeBase()
    # kb.add_paper("test1", "AI content", {"title": "T1", "authors": ["A1"], "pdf_url": "url"}, "Analysis result")
    
    memory = UserMemory()
    # memory.add_memory("Người dùng tên là Hải, thích nghiên cứu AI Agents.")
    # print(memory.get_relevant_memories("Tên người dùng là gì?"))
