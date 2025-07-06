# FILE: main_orchestrator.py
from rag.rag_service import RAGService
from agentes.agente_extrator_nlp_temporal import AgenteExtratorNLP_Temporal
from agentes.agente_analisador_imagem import AgenteAnalisadorDeImagem
from agentes.agente_gerador_hipoteses import AgenteGeradorDeHipoteses
from agentes.agente_analise_hipotese import AgenteAnaliseHipotese
from agentes.agente_sintese_comparativa import AgenteSinteseComparativa
from typing import Dict, Any, List, Optional

class OrquestradorDiferencial:
    def __init__(self):
        print("INFO: Inicializando o Orquestrador Diferencial e seus componentes...")
        self.rag_service = RAGService()
        self.agente_extrator = AgenteExtratorNLP_Temporal()
        self.agente_imagem = AgenteAnalisadorDeImagem()
        self.agente_gerador_hipoteses = AgenteGeradorDeHipoteses()
        self.agente_analise_hipotese = AgenteAnaliseHipotese(self.rag_service)
        self.agente_sintese = AgenteSinteseComparativa()
        
        self.memoria_conversa = {} # Simples memória para o último caso

    def executar_fluxo(self, texto_usuario: str, caminho_imagem: Optional[str] = None) -> str:
        print("\n--- INICIANDO NOVO FLUXO DE ANÁLISE ---")
        
        # 1. Extração e Percepção
        dados_caso = self.agente_extrator.executar(texto_usuario)
        self.memoria_conversa['dados_caso'] = dados_caso

        if caminho_imagem:
            analise_img = self.agente_imagem.executar(caminho_imagem)
            dados_caso['analise_imagem'] = analise_img
        
        # 2. Refinamento Interativo
        if dados_caso.get("necessita_info"):
            return f"Pergunta de Esclarecimento: {dados_caso['necessita_info']}"

        # 3. Geração de Hipóteses
        hipoteses = self.agente_gerador_hipoteses.executar(dados_caso['entidades'])
        if not hipoteses:
            return "Não foi possível gerar hipóteses diagnósticas com os dados fornecidos."
        self.memoria_conversa['hipoteses'] = hipoteses

        # 4. Análise Paralela
        relatorios_paralelos = []
        for h in hipoteses:
            if h is not None:
                 relatorio = self.agente_analise_hipotese.executar(h, dados_caso)
                 relatorios_paralelos.append(relatorio)

        # 5. Síntese Comparativa
        resultado_final = self.agente_sintese.executar(relatorios_paralelos)
        self.memoria_conversa['ultimo_resultado'] = resultado_final
        
        return resultado_final
