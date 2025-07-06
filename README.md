# FILE: README.md

---
title: LauderExam™ v3 - The Differential Engine
emoji: 🩺🧠
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 4.21.0
app_file: app.py
pinned: false
---

## 1. Descrição

O **LauderExam™ v3** é um sistema de IA multimodal e conversacional projetado para emular o processo de raciocínio de um médico especialista em diagnóstico. Esta aplicação web interativa permite que você:

-   **Descreva um caso clínico** em texto livre.
-   **Faça upload de imagens** ou documentos relevantes (opcional).
-   Receba uma **análise de diagnóstico diferencial** que avalia múltiplas hipóteses em paralelo.
-   Veja como o sistema utiliza uma **base de conhecimento (RAG)** para justificar suas conclusões.

## 2. Como Usar

1.  **Digite a descrição do paciente** no campo de chat na parte inferior. Seja o mais descritivo possível.
2.  (Opcional) Clique no botão de upload para anexar uma imagem.
3.  Clique em **"Analisar Caso"** e aguarde a resposta do sistema.

## 3. Arquitetura do Sistema

O sistema utiliza um orquestrador central que gerencia um fluxo de agentes especializados, incluindo processamento de linguagem e imagem, geração de hipóteses, análise paralela e síntese comparativa.

```mermaid
graph TD
    subgraph "Interface Multimodal (Gradio)"
        UI[💬 Chat com Upload de Arquivos]
    end
    subgraph "Orquestração e Raciocínio"
        O(OrquestradorDiferencial)
    end
    subgraph "Camada de Percepção e Extração"
        NLP(AgenteExtratorNLP_Temporal)
        CV(AgenteAnalisadorDeImagem)
        RAG(AgenteRecuperadorRAG)
        DB[(fa:fa-database Vector DB)]
    end
    subgraph "Motor de Análise Paralela"
        P(Análise Hipótese 1, 2, 3)
    end
    subgraph "Camada de Síntese"
        S(AgenteSinteseComparativa)
    end
    UI -- "Input" --> O --> NLP & CV
    NLP & CV --> O
    O -- "Gera Hipóteses e dispara" --> P
    P -- "Consulta" --> RAG -- "Busca" --> DB
    P -- "Relatórios" --> S --> O
    O -- "Resposta" --> UI
