"""
Frontend Streamlit para Model X AI Reasoning System.

Interface web completa com dashboard de métricas.

Uso:
    pip install streamlit plotly
    streamlit run frontend_streamlit.py

Acesse: http://localhost:8501
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Model X AI Reasoning",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTADO DA SESSÃO
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = f"streamlit-{int(time.time())}"

# ============================================================================
# FUNÇÕES
# ============================================================================

def check_api_status():
    """Verifica status da API."""
    try:
        response = requests.get(f"{API_URL}/docs", timeout=3)
        return response.status_code == 200
    except:
        return False


def send_message(message: str) -> dict:
    """Envia mensagem para a API."""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "conversation_id": st.session_state.conversation_id,
                "message": message,
                "is_new_conversation": len(st.session_state.messages) == 0
            },
            timeout=120
        )

        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"HTTP {response.status_code}"}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "API não disponível"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def interpret_x_state(x_value: float) -> tuple:
    """Interpreta o estado de X."""
    if x_value > 0.3:
        return "🔴 Alto Caos", "red", "STRUCTURING"
    elif x_value < -0.3:
        return "🔵 Alta Ordem", "blue", "EXPLORING"
    else:
        return "🟢 Equilíbrio", "green", "BALANCED"


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.image("https://em-content.zobj.net/source/twitter/376/robot_1f916.png", width=80)
    st.title("Model X AI")

    # Status
    st.markdown("### 📡 Status da API")
    if check_api_status():
        st.success("✅ Online")
    else:
        st.error("❌ Offline")
        st.code("uvicorn backend.main:app --port 8000")

    st.markdown("---")

    # Configurações
    st.markdown("### ⚙️ Configurações")

    generation_mode = st.selectbox(
        "Modo de Geração",
        ["reasoning", "simple", "chain", "reflective"],
        help="reasoning=balanceado, chain=detalhado, reflective=alta qualidade"
    )

    st.text_input(
        "ID da Conversa",
        value=st.session_state.conversation_id,
        key="conv_id_input",
        disabled=True
    )

    if st.button("🔄 Nova Conversa"):
        st.session_state.messages = []
        st.session_state.metrics_history = []
        st.session_state.conversation_id = f"streamlit-{int(time.time())}"
        st.rerun()

    st.markdown("---")

    # Métricas atuais
    st.markdown("### 📊 Última Métrica")
    if st.session_state.metrics_history:
        last = st.session_state.metrics_history[-1]
        state_label, state_color, strategy = interpret_x_state(last["X"])

        col1, col2 = st.columns(2)
        col1.metric("σ (entropia)", f"{last['sigma']:.3f}")
        col2.metric("S (sintropia)", f"{last['S']:.3f}")

        st.metric("X (saldo)", f"{last['X']:.3f}")
        st.markdown(f"**Estado:** {state_label}")
        st.markdown(f"**Estratégia:** `{strategy}`")

    st.markdown("---")

    # Info
    with st.expander("ℹ️ Sobre o Model X"):
        st.markdown("""
        **X = σ - S**

        - **σ**: Entropia (caos)
        - **S**: Sintropia (ordem)
        - **X**: Saldo de entropia

        | X | Estado | Ação |
        |---|--------|------|
        | >0.3 | Caos | Estruturar |
        | <-0.3 | Rígido | Explorar |
        | ±0.3 | OK | Balancear |
        """)

# ============================================================================
# ÁREA PRINCIPAL
# ============================================================================

st.title("🧠 Model X AI Reasoning System")
st.markdown("Sistema de IA com reasoning baseado no Model X (X = σ - S)")

# Tabs
tab_chat, tab_metrics, tab_history = st.tabs(["💬 Chat", "📈 Métricas", "📜 Histórico"])

# ============================================================================
# TAB: CHAT
# ============================================================================

with tab_chat:
    # Container para mensagens
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

                # Mostra métricas inline se for resposta do assistente
                if msg["role"] == "assistant" and "metrics" in msg:
                    m = msg["metrics"]
                    with st.expander("📊 Ver métricas", expanded=False):
                        cols = st.columns(4)
                        cols[0].metric("σ", f"{m['sigma']:.3f}")
                        cols[1].metric("S", f"{m['S']:.3f}")
                        cols[2].metric("X", f"{m['X']:.3f}")
                        cols[3].metric("Coerência", f"{m['coherence']:.1%}")

    # Input
    if prompt := st.chat_input("Digite sua mensagem..."):
        # Adiciona mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        # Envia para API
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                result = send_message(prompt)

            if result["success"]:
                data = result["data"]
                answer = data.get("answer_text", "Sem resposta")

                st.markdown(answer)

                # Salva métricas
                metrics = {
                    "sigma": data.get("sigma", 0),
                    "S": data.get("S", 0),
                    "X": data.get("X", 0),
                    "coherence": data.get("coherence_score", 0),
                    "timestamp": datetime.now().isoformat()
                }

                st.session_state.metrics_history.append(metrics)

                # Adiciona resposta ao histórico
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "metrics": metrics
                })

                # Mostra métricas
                with st.expander("📊 Ver métricas", expanded=False):
                    cols = st.columns(4)
                    cols[0].metric("σ", f"{metrics['sigma']:.3f}")
                    cols[1].metric("S", f"{metrics['S']:.3f}")
                    cols[2].metric("X", f"{metrics['X']:.3f}")
                    cols[3].metric("Coerência", f"{metrics['coherence']:.1%}")
            else:
                st.error(f"❌ Erro: {result['error']}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ Erro: {result['error']}"
                })

# ============================================================================
# TAB: MÉTRICAS
# ============================================================================

with tab_metrics:
    st.markdown("### 📈 Evolução das Métricas")

    if st.session_state.metrics_history:
        import pandas as pd

        df = pd.DataFrame(st.session_state.metrics_history)
        df["index"] = range(1, len(df) + 1)

        # Gráfico de linhas
        st.line_chart(df.set_index("index")[["sigma", "S", "X"]])

        # Tabela
        st.markdown("### 📋 Dados")
        st.dataframe(
            df[["sigma", "S", "X", "coherence"]].round(3),
            use_container_width=True
        )

        # Estatísticas
        st.markdown("### 📊 Estatísticas")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("σ médio", f"{df['sigma'].mean():.3f}")
        col2.metric("S médio", f"{df['S'].mean():.3f}")
        col3.metric("X médio", f"{df['X'].mean():.3f}")
        col4.metric("Coerência média", f"{df['coherence'].mean():.1%}")

    else:
        st.info("Envie mensagens no chat para ver as métricas aqui.")

# ============================================================================
# TAB: HISTÓRICO
# ============================================================================

with tab_history:
    st.markdown("### 📜 Histórico da Conversa")

    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            role_name = "Você" if msg["role"] == "user" else "Model X"

            with st.expander(f"{role_icon} {role_name} - Mensagem {i+1}", expanded=False):
                st.markdown(msg["content"])

                if "metrics" in msg:
                    st.json(msg["metrics"])

        # Download
        st.download_button(
            "📥 Baixar Histórico (JSON)",
            data=json.dumps(st.session_state.messages, indent=2, ensure_ascii=False),
            file_name=f"modelx_chat_{st.session_state.conversation_id}.json",
            mime="application/json"
        )
    else:
        st.info("Nenhuma mensagem ainda.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        Model X AI Reasoning System | Powered by Open Source LLMs
    </div>
    """,
    unsafe_allow_html=True
)
