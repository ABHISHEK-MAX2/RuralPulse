import chromadb
from chromadb.utils import embedding_functions

DB_DIR = "./chroma_db"
COLLECTION_NAME = "medical_triage"

class MedicalRetriever:
    def __init__(self, db_dir: str = DB_DIR, collection_name: str = COLLECTION_NAME):
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        self.client = chromadb.PersistentClient(path=db_dir)
        self.collection = self.client.get_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def get_top_k(self, query: str, k: int = 3):
        """Returns the top_k matching chunks for the query."""
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        extracted_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                extracted_results.append({
                    "text": doc,
                    "page": meta.get("page", "Unknown")
                })
        return extracted_results

    def get_context_string(self, query: str, k: int = 3) -> str:
        """Formats matches directly as a clean string Dev 3 can drop into Watsonx."""
        chunks = self.get_top_k(query, k=k)
        formatted = []
        for i, chunk in enumerate(chunks, 1):
            formatted.append(f"[Excerpt {i} | Page {chunk['page']}]:\n{chunk['text']}")
        return "\n\n---\n\n".join(formatted)


if __name__ == "__main__":
    # Quick test to verify Dev 2 works independently
    retriever = MedicalRetriever()
    test_query = "patient with severe chest pain, left arm numbness, sweating"
    
    print(f"Testing query: '{test_query}'\n")
    context = retriever.get_context_string(test_query, k=2)
    print("--- RETRIEVED MEDICAL CONTEXT ---")
    print(context)