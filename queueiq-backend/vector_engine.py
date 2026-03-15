import chromadb
import os
import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = "models/embedding-001"
        title = "Hospital SOP Document"
        embeddings = genai.embed_content(model=model,
                                        content=input,
                                        task_type="retrieval_document",
                                        title=title)["embedding"]
        return embeddings

class VectorEngine:
    def __init__(self):
        # Configure genai if not already configured in main.py
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.emb_fn = GeminiEmbeddingFunction()
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
        print("Vector store seeded with Gemini embeddings.")

    def query(self, text: str, n_results: int = 2):
        try:
            results = self.collection.query(
                query_texts=[text],
                n_results=n_results
            )
            return results["documents"][0] if results["documents"] else []
        except Exception as e:
            print(f"Vector Query Error: {e}")
            return []

# Global singleton
_vector_engine = None

def get_vector_engine():
    global _vector_engine
    if _vector_engine is None:
        try:
            _vector_engine = VectorEngine()
        except Exception as e:
            print(f"Vector Engine Lazy Init Error: {e}")
            return None
    return _vector_engine

def init_vector_store():
    """Initializes and seeds the vector store. Called on app startup."""
    try:
        engine = get_vector_engine()
        if engine:
            engine.seed_knowledge("./knowledge_base")
    except Exception as e:
        print(f"Vector Store Initialization Warning: {e}")
