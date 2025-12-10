from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
import time
import os

from .conversation_state import ConversationState, update_rhythm_stats, append_message
from .coding_engineering.interpret import classify_coding_subdomain
from .domains import compute_energy_vector
from .energy_model import adjust_energy_with_rhythm, compute_sigma_S_from_energy
from .modelx_core import evaluate_system_with_model_x
from .coding_engineering.generator import generate_answer
from .coding_engineering.coherence_evaluator import evaluate_coherence
from .meta_learning import update_parameters

# Importa novos módulos de web e aprendizado
try:
    from .web_tools import smart_search, needs_web
    from .learning_memory import get_memory, save_interaction, get_context
    WEB_AND_LEARNING_AVAILABLE = True
except ImportError:
    WEB_AND_LEARNING_AVAILABLE = False


app = FastAPI(
    title="Model X Agent API",
    description="Assistente de IA com reasoning baseado no Modelo X (X = σ − S), acesso à web e aprendizado contínuo",
    version="2.0.0"
)

# Configuração de CORS para permitir acesso de outros domínios
# AVISO DE SEGURANÇA: allow_origins=["*"] permite requisições de qualquer domínio.
# Em produção, substitua ["*"] pelas origens específicas permitidas, por exemplo:
# allow_origins=["https://seu-frontend.netlify.app", "https://seudominio.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure com suas origens específicas em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Em um sistema real, isso deve ir para algum store (cache/DB)
CONVERSATIONS: Dict[str, ConversationState] = {}


class ChatRequest(BaseModel):
    conversation_id: str
    message: str
    is_new_conversation: bool = False
    enable_web_search: bool = True  # Habilita busca web automática
    enable_learning: bool = True    # Habilita aprendizado


class ChatResponse(BaseModel):
    answer_text: str
    sigma: float
    S: float
    X: float
    x_interpretation: str
    energy_vector: Dict[str, float]
    coherence_score: float
    # Novos campos
    web_search_used: bool = False
    web_sources: List[str] = []
    learning_context_used: bool = False


def get_or_create_conversation(req: ChatRequest) -> ConversationState:
    if req.is_new_conversation or req.conversation_id not in CONVERSATIONS:
        state = ConversationState(
            id=req.conversation_id,
            root_question=req.message,
            root_question_vector=None  # TODO: calcular embedding
        )
        CONVERSATIONS[req.conversation_id] = state
    else:
        state = CONVERSATIONS[req.conversation_id]
    return state


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    ts = time.time()
    state = get_or_create_conversation(req)

    # 1) atualizar ritmo e logar mensagem do usuário
    rhythm = update_rhythm_stats(state, req.message, ts)
    append_message(state, "user", req.message, ts)

    # 2) classificar domínio/subdomínio (fixo coding_engineering por enquanto)
    domain_info = classify_coding_subdomain(req.message)

    # 3) vetor de energia base
    E_base = compute_energy_vector(domain_info)

    # 4) ajuste com ritmo
    E = adjust_energy_with_rhythm(E_base, rhythm)

    # 5) σ, S, X
    sigma_S_X = compute_sigma_S_from_energy(E)

    # 6) construir "system" e avaliar com Modelo X (interpretação genérica)
    system = {
        "domain": domain_info["domain"],
        "energy_vector": E,
        **sigma_S_X
    }
    x_result = evaluate_system_with_model_x(system)

    # === NOVOS RECURSOS ===
    web_search_used = False
    web_sources = []
    learning_context_used = False
    extra_context = ""

    if WEB_AND_LEARNING_AVAILABLE:
        # 6.1) Busca na web se necessário
        if req.enable_web_search and needs_web(req.message):
            web_result = smart_search(req.message)
            if web_result.get("searched"):
                web_search_used = True
                web_sources = web_result.get("sources", [])
                extra_context += "\n" + web_result.get("content", "")

        # 6.2) Busca contexto de interações anteriores
        if req.enable_learning:
            memory = get_memory(req.conversation_id)
            learning_ctx = memory.get_context_prompt(req.message)
            if learning_ctx:
                learning_context_used = True
                extra_context += "\n" + learning_ctx

            # Adiciona preferências do usuário
            prefs_ctx = memory.get_preferences_prompt()
            if prefs_ctx:
                extra_context += "\n" + prefs_ctx

    # Adiciona contexto extra ao state para o generator usar
    if extra_context:
        state.extra_context = extra_context

    # 7) gerar resposta
    answer = generate_answer(req.message, E, sigma_S_X, state)

    # 8) avaliar coerência (compilação, testes, alinhamento com pergunta-raiz)
    feedback = evaluate_coherence(req.message, answer, state)

    # 9) meta-ajuste global
    update_parameters(feedback, domain=domain_info["domain"])

    # 10) logar resposta na conversa
    append_message(state, "assistant", answer["answer_text"], time.time())
    state.coherence_history.append(feedback)

    # 11) Salvar interação para aprendizado
    if WEB_AND_LEARNING_AVAILABLE and req.enable_learning:
        save_interaction(
            question=req.message,
            answer=answer["answer_text"],
            feedback_score=feedback["coherence_score"],
            user_id=req.conversation_id,
            metadata={
                "sigma": x_result["sigma"],
                "S": x_result["S"],
                "X": x_result["X"],
                "web_used": web_search_used
            }
        )

    return ChatResponse(
        answer_text=answer["answer_text"],
        sigma=x_result["sigma"],
        S=x_result["S"],
        X=x_result["X"],
        x_interpretation=x_result["interpretation"],
        energy_vector=E,
        coherence_score=feedback["coherence_score"],
        web_search_used=web_search_used,
        web_sources=web_sources,
        learning_context_used=learning_context_used
    )


# === NOVOS ENDPOINTS ===

class FeedbackRequest(BaseModel):
    conversation_id: str
    interaction_id: Optional[str] = None
    feedback_score: float  # -1 a 1


@app.post("/feedback")
def submit_feedback(req: FeedbackRequest):
    """
    Envia feedback sobre uma resposta para melhorar o aprendizado.

    feedback_score:
    - 1.0: Excelente resposta
    - 0.5: Boa resposta
    - 0.0: Resposta neutra
    - -0.5: Resposta ruim
    - -1.0: Resposta muito ruim
    """
    if not WEB_AND_LEARNING_AVAILABLE:
        return {"success": False, "error": "Learning module not available"}

    memory = get_memory(req.conversation_id)

    # Se não especificou interaction_id, usa a última
    if req.interaction_id:
        memory.update_feedback(req.interaction_id, req.feedback_score)
    elif memory.interactions:
        last_id = memory.interactions[-1].id
        memory.update_feedback(last_id, req.feedback_score)

    return {"success": True, "message": "Feedback registrado com sucesso"}


@app.get("/stats/{conversation_id}")
def get_stats(conversation_id: str):
    """Retorna estatísticas de aprendizado de uma conversa."""
    if not WEB_AND_LEARNING_AVAILABLE:
        return {"error": "Learning module not available"}

    memory = get_memory(conversation_id)
    return memory.get_stats()


@app.get("/learning-summary/{conversation_id}")
def get_learning_summary(conversation_id: str):
    """Retorna resumo do que foi aprendido."""
    if not WEB_AND_LEARNING_AVAILABLE:
        return {"error": "Learning module not available"}

    memory = get_memory(conversation_id)
    return {"summary": memory.get_learning_summary()}


@app.get("/status")
def get_status():
    """Retorna status do sistema e recursos disponíveis."""
    status = {
        "api_version": "2.0.0",
        "model_x": True,
        "web_search": WEB_AND_LEARNING_AVAILABLE,
        "learning_memory": WEB_AND_LEARNING_AVAILABLE,
    }

    # Verifica provedores LLM
    try:
        from .llm_providers import get_default_provider
        provider = get_default_provider()
        status["llm_providers"] = provider.get_status()
    except ImportError:
        status["llm_providers"] = {"available": False}

    return status


# Endpoint para servir o frontend (desenvolvimento/testes)
# Em produção, o frontend deve ser servido por um servidor estático separado
@app.get("/")
async def serve_frontend():
    """Serve the frontend index.html"""
    frontend_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "frontend",
        "index.html"
    )
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type="text/html")
    return {"message": "Frontend not found. API is running at /chat"}
