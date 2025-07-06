# FILE: agentes/agente_gerador_hipoteses.py
from typing import List, Dict

class AgenteGeradorDeHipoteses:
    def __init__(self):
        self.mapa_hipoteses = {
            "Tromboembolismo Pulmonar (TEP)": ["dispneia", "d-dímero", "dor no peito"],
            "Pneumonia Bacteriana": ["febre", "tosse", "leucócitos"],
            "Infarto Agudo do Miocárdio": ["dor no peito", "troponina", "fadiga"]
        }

    def executar(self, entidades: Dict) -> List[str]:
        print(f"INFO: Agente '{self.__class__.__name__}' executando...")
        scores = {hipotese: 0 for hipotese in self.mapa_hipoteses}
        achados = entidades.get("achados", [])
        
        for hipotese, palavras_chave in self.mapa_hipoteses.items():
            for achado in achados:
                if any(palavra in achado for palavra in palavras_chave):
                    scores[hipotese] += 1
        
        hipoteses_ordenadas = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
        return [h for h in hipoteses_ordenadas if scores[h] > 0][:3]
