# FILE: rag/knowledge_base_content.py
def get_knowledge_chunks() -> list[str]:
    """
    Retorna uma lista de trechos de conhecimento médico.
    Em um sistema real, isso viria de documentos, APIs, etc.
    """
    return [
        "Achado: Opacidades em vidro fosco. Contexto: Este é um achado radiológico inespecífico. Em um contexto de infecção aguda com febre, pode sugerir pneumonia viral, como por Influenza ou COVID-19. Em um paciente com doença do tecido conjuntivo, pode indicar doença pulmonar intersticial.",
        "Achado: D-dímero elevado. Contexto: Um D-dímero elevado indica a presença de produtos de degradação da fibrina. É sensível, mas não específico. Em um paciente com dispneia súbita e fatores de risco (viagem longa, imobilização), aumenta a suspeita de Tromboembolismo Pulmonar (TEP). Também se eleva em infecções graves (sepse), traumas e câncer.",
        "Achado: Leucocitose com desvio à esquerda. Contexto: Aumento de leucócitos com presença de formas jovens (bastonetes) é um forte indicativo de infecção bacteriana aguda. O corpo está respondendo a uma invasão bacteriana produzindo mais neutrófilos.",
        "Achado: Enzimas cardíacas elevadas (Troponina). Contexto: A troponina é um marcador altamente específico de lesão miocárdica. Sua elevação em um paciente com dor torácica é o pilar para o diagnóstico de Infarto Agudo do Miocárdio. Níveis também podem subir em miocardite ou embolia pulmonar maciça.",
        "Hipótese: Tromboembolismo Pulmonar (TEP). Evidências a favor: Dispneia súbita, dor torácica pleurítica, taquicardia, D-dímero elevado, histórico de imobilização. Evidências contra: Febre alta, expectoração purulenta, ausência de fatores de risco para trombose.",
        "Hipótese: Pneumonia Bacteriana Comunitária. Evidências a favor: Febre, tosse produtiva, leucocitose com desvio à esquerda, consolidação em radiografia de tórax. Evidências contra: Início súbito sem sintomas prodrômicos, D-dímero muito elevado sem outros sinais de inflamação sistêmica.",
        "Hipótese: Infarto Agudo do Miocárdio. Evidências a favor: Dor torácica opressiva com irradiação, troponina elevada, alterações em eletrocardiograma (ECG). Evidências contra: Dor de característica pleurítica (piora com a respiração), febre, ausência de fatores de risco cardiovascular."
    ]
Use code with caution.
Python
rag/rag_service.py
Generated python
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
