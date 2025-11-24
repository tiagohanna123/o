from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
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


app = FastAPI(
    title="Model X Agent API",
    description="Assistente de engenharia de software baseado no Modelo X (X = σ − S)",
    version="1.0.0"
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


class ChatResponse(BaseModel):
    answer_text: str
    sigma: float
    S: float
    X: float
    x_interpretation: str
    energy_vector: Dict[str, float]
    coherence_score: float


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

    # 7) gerar resposta
    answer = generate_answer(req.message, E, sigma_S_X, state)

    # 8) avaliar coerência (compilação, testes, alinhamento com pergunta-raiz)
    feedback = evaluate_coherence(req.message, answer, state)

    # 9) meta-ajuste global
    update_parameters(feedback, domain=domain_info["domain"])

    # 10) logar resposta na conversa
    append_message(state, "assistant", answer["answer_text"], time.time())
    state.coherence_history.append(feedback)

    return ChatResponse(
        answer_text=answer["answer_text"],
        sigma=x_result["sigma"],
        S=x_result["S"],
        X=x_result["X"],
        x_interpretation=x_result["interpretation"],
        energy_vector=E,
        coherence_score=feedback["coherence_score"]
    )


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
