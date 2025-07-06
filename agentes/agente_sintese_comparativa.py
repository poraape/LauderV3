# FILE: agentes/agente_sintese_comparativa.py
from typing import List, Dict, Any

class AgenteSinteseComparativa:
    def executar(self, relatorios_paralelos: List[Dict[str, Any]]) -> str:
        """
        Recebe os relatórios de análise de cada hipótese e os compila em uma
        única resposta comparativa e formatada.
        """
        print(f"INFO: Agente '{self.__class__.__name__}' executando...")
        
        if not relatorios_paralelos:
            return "Não foi possível gerar uma análise com os dados fornecidos."

        # Ordena os relatórios pelo score de confiança, do maior para o menor
        relatorios_ordenados = sorted(relatorios_paralelos, key=lambda r: r['score_confianca'], reverse=True)
        
        # Constrói a string de saída em formato Markdown
        output = "## Análise Diagnóstica Diferencial Comparativa\n\n"
        output += "Com base nos dados fornecidos, foram avaliadas as seguintes hipóteses em paralelo:\n\n"
        
        for i, rel in enumerate(relatorios_ordenados):
            if i == 0:
                output += f"### **Hipótese Principal: {rel['hipotese']}**\n"
            else:
                output += f"### **Hipótese Alternativa: {rel['hipotese']}**\n"
                
            output += f"- **Nível de Confiança:** {rel['score_confianca']}%\n"
            output += f"- **Justificativa:** {rel['justificativa']}\n"
            
            if rel['evidencias_rag']:
                output += "- **Evidências Relevantes da Base de Conhecimento:**\n"
                for ev in rel['evidencias_rag']:
                    output += f"  - *{ev}*\n"
            else:
                output += "- **Evidências Relevantes da Base de Conhecimento:** Nenhuma encontrada.\n"
            
            output += "\n"
            
        output += "---\n*AVISO: Este é um laudo gerado por um sistema de IA e não substitui uma avaliação médica profissional.*"
        
        return output
