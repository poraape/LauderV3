# FILE: agentes/agente_extrator_nlp_temporal.py
import spacy
import re
from typing import Dict, Any

class AgenteExtratorNLP_Temporal:
    def __init__(self):
        print("INFO: Carregando modelo spaCy (pt_core_news_lg)...")
        try:
            self.nlp = spacy.load("pt_core_news_lg")
        except OSError:
            print("ERRO: Modelo 'pt_core_news_lg' não encontrado. Execute 'python -m spacy download pt_core_news_lg'")
            self.nlp = None
        
        self.patterns = {
            "EXAME": [r"d-dímero", r"pcr", r"troponina", r"leucócitos"],
            "SINTOMA": [r"dispneia", r"tosse", r"febre", r"dor no peito", r"fadiga"],
            "TEMPO": [r"há \d+ dias", r"desde ontem", r"progressiva"]
        }

    def executar(self, texto: str) -> Dict[str, Any]:
        print(f"INFO: Agente '{self.__class__.__name__}' executando...")
        if not self.nlp:
            return {"entidades": {}, "necessita_info": "Modelo de linguagem não carregado."}

        doc = self.nlp(texto.lower())
        entidades = {"achados": [], "timeline": []}

        for label, patterns in self.patterns.items():
            for pattern in patterns:
                for match in re.finditer(pattern, texto.lower()):
                    if label in ["EXAME", "SINTOMA"]:
                        entidades["achados"].append(match.group(0))
                    elif label == "TEMPO":
                        entidades["timeline"].append(match.group(0))
        
        entidades["achados"] = list(set(entidades["achados"]))
        entidades["timeline"] = list(set(entidades["timeline"]))

        necessita_info = False
        if "dor no peito" in entidades["achados"] and not any(kw in texto.lower() for kw in ["opressiva", "pleurítica", "pontada"]):
             necessita_info = "Você mencionou 'dor no peito'. Poderia descrever melhor o tipo da dor (ex: em aperto, pontada, queimação)?"

        return {"entidades": entidades, "necessita_info": necessita_info}
