# FILE: rag/rag_service.py
import chromadb
from chromadb.utils import embedding_functions
from typing import List
import os

class RAGService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.db_path = "chroma_db"
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)
        self.collection = self.client.get_or_create_collection(
            name="lauder_exam_kb",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"INFO: Serviço RAG com ChromaDB inicializado. Dados em: '{self.db_path}'")

    def populate_knowledge_base(self, chunks: List[str]):
        print(f"INFO: Populando a base de conhecimento com {len(chunks)} trechos...")
        count = self.collection.count()
        if count > 0:
            print(f"INFO: Limpando {count} itens antigos da coleção.")
            existing_ids = self.collection.get(include=[])['ids']
            if existing_ids:
                self.collection.delete(ids=existing_ids)

        ids = [f"chunk_{i}" for i in range(len(chunks))]
        self.collection.add(documents=chunks, ids=ids)
        print("INFO: Base de conhecimento populada com sucesso.")

    def search(self, query: str, k: int = 3) -> List[str]:
        if self.collection.count() == 0:
            return ["Erro: A base de conhecimento está vazia. Execute 'setup_rag.py' primeiro."]
        results = self.collection.query(query_texts=[query], n_results=k)
        return results['documents'][0] if results['documents'] else []
