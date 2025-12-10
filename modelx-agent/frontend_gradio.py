"""
Frontend Gradio para Model X AI Reasoning System.

Gera automaticamente uma interface web interativa para a IA.

Uso:
    pip install gradio
    python frontend_gradio.py

Acesse: http://localhost:7860
"""

import gradio as gr
import requests
import json
from typing import Tuple, List

# Configuração
API_URL = "http://localhost:8000"


def chat_with_modelx(
    message: str,
    history: List[Tuple[str, str]],
    conversation_id: str,
    generation_mode: str
) -> Tuple[str, List[Tuple[str, str]], str]:
    """Envia mensagem para a API do Model X e retorna resposta."""

    if not message.strip():
        return "", history, "Digite uma mensagem"

    try:
        # Faz requisição para a API
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "conversation_id": conversation_id or "gradio-session",
                "message": message,
                "is_new_conversation": len(history) == 0
            },
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()

            # Formata métricas do Model X
            metrics = f"""
**Métricas Model X:**
- σ (entropia): {data.get('sigma', 0):.3f}
- S (sintropia): {data.get('S', 0):.3f}
- X (saldo): {data.get('X', 0):.3f}
- Coerência: {data.get('coherence_score', 0):.1%}

**Interpretação:** {data.get('x_interpretation', 'N/A')}
"""

            # Atualiza histórico
            history.append((message, data.get('answer_text', 'Sem resposta')))

            return "", history, metrics
        else:
            return "", history, f"Erro: {response.status_code} - {response.text[:200]}"

    except requests.exceptions.ConnectionError:
        return "", history, "❌ Erro: Não foi possível conectar à API. Inicie o servidor com: uvicorn backend.main:app --port 8000"
    except Exception as e:
        return "", history, f"❌ Erro: {str(e)}"


def clear_chat() -> Tuple[List, str]:
    """Limpa o chat."""
    return [], ""


def get_system_status() -> str:
    """Obtém status do sistema."""
    try:
        # Tenta obter info do modelo
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            return "✅ API Online - Conectado ao Model X Agent"
        return "⚠️ API parcialmente disponível"
    except:
        return "❌ API Offline - Execute: uvicorn backend.main:app --port 8000"


# ============================================================================
# INTERFACE GRADIO
# ============================================================================

with gr.Blocks(
    title="Model X AI Reasoning",
    theme=gr.themes.Soft(primary_hue="blue"),
    css="""
    .metrics-box { background: #f0f4f8; padding: 15px; border-radius: 8px; }
    .status-online { color: green; }
    .status-offline { color: red; }
    """
) as demo:

    # Header
    gr.Markdown("""
    # 🧠 Model X AI Reasoning System

    Sistema de IA que usa o **Model X (X = σ - S)** como lógica de reasoning,
    integrado com LLMs open source gratuitos.

    ---
    """)

    with gr.Row():
        # Coluna principal - Chat
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                label="Conversa",
                height=500,
                show_copy_button=True,
                avatar_images=(None, "https://em-content.zobj.net/source/twitter/376/robot_1f916.png")
            )

            with gr.Row():
                msg_input = gr.Textbox(
                    label="Sua mensagem",
                    placeholder="Digite sua pergunta sobre engenharia de software, Model X, ou qualquer assunto...",
                    lines=2,
                    scale=4
                )
                send_btn = gr.Button("Enviar", variant="primary", scale=1)

            with gr.Row():
                clear_btn = gr.Button("🗑️ Limpar Chat")

        # Coluna lateral - Configurações e Métricas
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Configurações")

            conversation_id = gr.Textbox(
                label="ID da Conversa",
                value="gradio-session",
                info="Identificador único da sessão"
            )

            generation_mode = gr.Dropdown(
                label="Modo de Geração",
                choices=["reasoning", "simple", "chain", "reflective"],
                value="reasoning",
                info="reasoning=balanceado, chain=detalhado, reflective=alta qualidade"
            )

            gr.Markdown("### 📊 Métricas Model X")
            metrics_display = gr.Markdown(
                value="*Envie uma mensagem para ver as métricas*",
                elem_classes=["metrics-box"]
            )

            gr.Markdown("### 📡 Status")
            status_display = gr.Markdown(value=get_system_status())
            refresh_btn = gr.Button("🔄 Atualizar Status")

    # Exemplos
    gr.Markdown("### 💡 Exemplos de Perguntas")
    gr.Examples(
        examples=[
            ["O que é entropia (σ) no Model X?"],
            ["Como o valor de X influencia o reasoning?"],
            ["Explique como otimizar queries SQL lentas"],
            ["Quais são as melhores práticas para testes unitários?"],
            ["Como implementar autenticação JWT em Python?"],
            ["Explique arquitetura hexagonal com exemplos"],
        ],
        inputs=msg_input
    )

    # Informações
    with gr.Accordion("ℹ️ Sobre o Model X", open=False):
        gr.Markdown("""
        ## O que é o Model X?

        O **Model X** é um framework matemático para análise de complexidade baseado em:

        - **σ (sigma)**: Entropia - mede desordem, incerteza, caos
        - **S**: Sintropia - mede ordem, estrutura, organização
        - **X = σ - S**: Saldo de entropia

        ### Como o X influencia o reasoning:

        | Valor de X | Estado | Estratégia |
        |------------|--------|------------|
        | X > 0.3 | Alto caos | STRUCTURING - foca em clareza |
        | X < -0.3 | Alta ordem | EXPLORING - questiona premissas |
        | -0.3 ≤ X ≤ 0.3 | Equilíbrio | BALANCED - abordagem natural |

        ### Provedores LLM Suportados:
        - **Ollama** (local, gratuito)
        - **Groq** (cloud, muito rápido)
        - **Hugging Face** (cloud, gratuito)
        - **Together.ai** (cloud, créditos grátis)
        """)

    # Event handlers
    msg_input.submit(
        chat_with_modelx,
        inputs=[msg_input, chatbot, conversation_id, generation_mode],
        outputs=[msg_input, chatbot, metrics_display]
    )

    send_btn.click(
        chat_with_modelx,
        inputs=[msg_input, chatbot, conversation_id, generation_mode],
        outputs=[msg_input, chatbot, metrics_display]
    )

    clear_btn.click(
        clear_chat,
        outputs=[chatbot, metrics_display]
    )

    refresh_btn.click(
        get_system_status,
        outputs=[status_display]
    )


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║         Model X AI Reasoning - Frontend Gradio               ║
    ╠══════════════════════════════════════════════════════════════╣
    ║  1. Certifique-se que a API está rodando:                    ║
    ║     uvicorn backend.main:app --port 8000                     ║
    ║                                                              ║
    ║  2. Acesse: http://localhost:7860                            ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # Mude para True para criar link público
    )
