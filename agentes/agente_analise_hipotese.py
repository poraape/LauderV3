FILE: agentes/agente_analise_hipotese.py
from rag.rag_service import RAGService
from typing import Dict, Any
class AgenteAnaliseHipotese:
def init(self, rag_service: RAGService):
self.rag_service = rag_service

def executar(self, hipotese: str, dados_caso: Dict) -> Dict[str, Any]:
    print(f"INFO: Analisando hipótese em paralelo: '{hipotese}'...")
    
    query_rag = f"Evidências a favor e contra para a hipótese: {hipotese}, considerando os achados {', '.join(dados_caso['entidades']['achados'])}"
    contexto_rag = self.rag_service.search(query_rag, k=2)
    
    score = 50
    for achado in dados_caso['entidades']['achados']:
        if achado.lower() in hipotese.lower():
            score += 15
    
    relatorio = {
        "hipotese": hipotese,
        "score_confianca": min(score, 100),
        "evidencias_rag": contexto_rag,
        "justificativa": f"A confiança foi calculada com base nos achados do paciente e no conhecimento recuperado sobre '{hipotese}'."
    }
    return relatorio
