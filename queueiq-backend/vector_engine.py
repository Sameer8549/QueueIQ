import chromadb
from chromadb.utils import embedding_functions
import os

class VectorEngine:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="hospital_sops",
            embedding_function=self.emb_fn
        )
        
    def seed_knowledge(self, knowledge_dir: str):
        if not os.path.exists(knowledge_dir):
            return
            
        for filename in os.listdir(knowledge_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(knowledge_dir, filename), "r") as f:
                    content = f.read()
                    self.collection.upsert(
                        documents=[content],
                        ids=[filename],
                        metadatas=[{"source": filename}]
                    )
        print("Vector store seeded.")

    def query(self, text: str, n_results: int = 2):
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []

# Global instance
vector_engine = VectorEngine()
vector_engine.seed_knowledge("./knowledge_base")
