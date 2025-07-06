# FILE: app.py
import gradio as gr
from main_orchestrator import OrquestradorDiferencial
from rag.rag_service import RAGService
from rag.knowledge_base_content import get_knowledge_chunks
import time
import os

# --- LÓGICA DE AUTOINICIALIZAÇÃO PARA DEPLOYMENT ---
# Esta seção garante que a aplicação possa se configurar sozinha na nuvem.

def setup_knowledge_base():
    """
    Verifica se a base de conhecimento existe e, se não, a cria.
    """
    db_path = "chroma_db"
    # A verificação é simples: a pasta existe?
    if not os.path.exists(db_path):
        print("INFO: Base de conhecimento não encontrada. Iniciando processo de criação...")
        print("INFO: Este processo só ocorrerá na primeira inicialização do Space.")
        
        # Pega os trechos de conhecimento
        chunks = get_knowledge_chunks()
        if not chunks:
            print("ERRO FATAL: Nenhum trecho de conhecimento encontrado para popular o banco de dados.")
            return

        # Instancia o serviço RAG e popula a base
        rag_service = RAGService()
        rag_service.populate_knowledge_base(chunks)
        
        print("INFO: Base de conhecimento criada com sucesso.")
    else:
        print(f"INFO: Base de conhecimento encontrada em '{db_path}'. Inicialização normal.")

# Executa a verificação e o setup no momento em que a aplicação é iniciada
setup_knowledge_base()
# --- FIM DA LÓGICA DE AUTOINICIALIZAÇÃO ---


# --- INICIALIZAÇÃO DO ORQUESTRADOR E DA INTERFACE ---
print("INFO: Inicializando o Orquestrador Diferencial...")
orquestrador = OrquestradorDiferencial()
print("INFO: Aplicação Gradio pronta para ser lançada.")


def stream_response(message: str, history: list, file_path: str | None):
    """
    Função de streaming para a interface de chat.
    """
    print(f"INFO: Nova requisição recebida. Mensagem: '{message[:50]}...'. Arquivo: {file_path}")
    
    resultado_completo = orquestrador.executar_fluxo(message, file_path)
    
    buffer = ""
    for char in resultado_completo:
        buffer += char
        yield buffer
        time.sleep(0.01)

# Interface Gradio (sem mudanças na UI)
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky"), css=".gradio-container {max-width: 960px !important; margin: auto;}") as demo:
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1>🩺 LauderExam™ v3</h1>
            <p><strong>The Differential Engine</strong>: Análise Clínica Multimodal com Raciocínio Paralelo</p>
        </div>
        """
    )
    
    gr.ChatInterface(
        fn=stream_response,
        chatbot=gr.Chatbot(height=600, show_copy_button=True, bubble_full_width=False),
        textbox=gr.Textbox(placeholder="Descreva o caso clínico aqui...", container=False, scale=7),
        additional_inputs=[gr.File(label="Upload de Imagem ou Documento (Opcional)", type="filepath")],
        submit_btn="Analisar Caso",
        retry_btn="Tentar Novamente",
        undo_btn="Desfazer",
        clear_btn="Limpar Chat",
        title=None,
        examples=[
            ["Paciente com dispneia súbita e dor no peito há 1 dia. D-dímero elevado."],
            ["Homem, 65 anos, com febre alta e tosse produtiva há 3 dias. Leucócitos aumentados."],
        ]
    )
    
    gr.Markdown(
        """
        <div style="text-align: center; font-size: small; color: grey;">
            <p>Aviso: Este é um sistema de IA para fins de demonstração e não substitui uma avaliação médica profissional.</p>
        </div>
        """
    )

# O Gradio no Hugging Face Spaces procura por uma variável chamada 'demo' para lançar.
# Não precisamos mais do bloco if __name__ == "__main__": demo.launch()
