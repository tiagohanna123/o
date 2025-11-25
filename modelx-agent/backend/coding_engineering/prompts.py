from typing import Dict, List, Optional
from pathlib import Path


# Carrega o conhecimento oficial do Modelo X uma única vez no nível do módulo
def _load_modelo_x_knowledge() -> str:
    """Carrega o conteúdo de docs/modelo_x.md como conhecimento oficial."""
    # Navega do diretório atual até a raiz do repositório
    current_dir = Path(__file__).resolve().parent
    # backend/coding_engineering -> backend -> modelx-agent -> raiz do repo
    repo_root = current_dir.parent.parent.parent
    modelo_x_path = repo_root / "docs" / "modelo_x.md"
    
    if modelo_x_path.exists():
        return modelo_x_path.read_text(encoding="utf-8")
    
    # Fallback: conhecimento mínimo embutido
    return """
# Modelo X (X = σ − S) — Conhecimento Básico

- **σ (sigma)**: Entropia / desordem / incerteza / caos
- **S**: Sintropia / ordem / estrutura / organização
- **X = σ − S**: Saldo de entropia
  - X > 0: muita confusão, pouca estrutura
  - X ≈ 0: equilíbrio saudável
  - X < 0: estrutura demais, rigidez
"""


MODELO_X_KNOWLEDGE = _load_modelo_x_knowledge()


def _format_energy_vector(energy_vector: Dict[str, float]) -> str:
    """Formata o vetor de energia de forma legível."""
    lines = []
    for key, value in energy_vector.items():
        lines.append(f"  - {key}: {value:.3f}")
    return "\n".join(lines)


def _format_recent_history(state, max_turns: int = 5) -> str:
    """Formata os últimos turnos da conversa."""
    if not hasattr(state, 'messages') or not state.messages:
        return "(Início da conversa)"
    
    recent = state.messages[-max_turns * 2:]  # últimos N turnos (usuário + assistente)
    
    if not recent:
        return "(Início da conversa)"
    
    lines = []
    for msg in recent:
        role_label = "Usuário" if msg.role == "user" else "Assistente"
        # Trunca mensagens muito longas para o resumo
        content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
        lines.append(f"[{role_label}]: {content}")
    
    return "\n".join(lines)


def _interpret_x_state(sigma: float, S: float, X: float) -> str:
    """Gera uma interpretação qualitativa do estado de X."""
    if X > 0.3:
        return f"Estado de ALTA ENTROPIA (X = {X:.3f}). Há muita incerteza/confusão. Considere clarear requisitos ou reduzir escopo."
    elif X < -0.3:
        return f"Estado de ALTA SINTROPIA (X = {X:.3f}). Há muita rigidez/estrutura. Considere explorar alternativas ou simplificar."
    else:
        return f"Estado de EQUILÍBRIO (X = {X:.3f}). Balanço saudável entre exploração e estrutura."


def build_main_prompt(message: str, state, energy_vector: Dict[str, float], sigma_S_X: Dict[str, float]) -> str:
    """
    Constrói o prompt principal para o Model X Agent.
    
    Args:
        message: Mensagem atual do usuário.
        state: Estado da conversa (ConversationState).
        energy_vector: Vetor de energia em 10 dimensões.
        sigma_S_X: Dicionário com valores de sigma, S e X.
    
    Returns:
        Prompt estruturado para o LLM.
    """
    root_q = state.root_question
    sigma = sigma_S_X["sigma"]
    S = sigma_S_X["S"]
    X = sigma_S_X["X"]
    
    # Formata componentes do prompt
    energy_formatted = _format_energy_vector(energy_vector)
    history_formatted = _format_recent_history(state)
    x_interpretation = _interpret_x_state(sigma, S, X)

    prompt = f"""Você é o Model X Agent, um assistente de IA especializado em engenharia de software e no Modelo X (X = σ − S).

=== IDENTIDADE ===
- Seu nome é Model X Agent.
- Você é especialista em engenharia de software: debugging, refatoração, arquitetura, sprints, testes, etc.
- Você usa o Modelo X para analisar e melhorar sessões de trabalho.

=== IDIOMA ===
- Responda sempre em **PORTUGUÊS** por padrão.
- Só responda em outro idioma se:
  - O usuário escrever a mensagem claramente em outro idioma E mantiver esse padrão, OU
  - O usuário pedir explicitamente outro idioma.

<<<CONHECIMENTO_OFICIAL_MODELO_X>>>
{MODELO_X_KNOWLEDGE}
<<<FIM_CONHECIMENTO>>>

=== REGRAS SOBRE O MODELO X ===
- Você DEVE seguir o documento acima ao falar de σ, S, X, entropia e sintropia.
- Você NÃO PODE inventar novas fórmulas nem redefinir σ e S de forma incompatível.
- σ (sigma) SEMPRE significa entropia/desordem/incerteza/caos.
- S SEMPRE significa sintropia/ordem/estrutura/organização.
- X = σ − S SEMPRE é o saldo de entropia.
- Nunca use interpretações como "syntactic entropy" ou "semantic significance" para σ e S.

=== ESTADO ATUAL DO MODELO X ===
Valores atuais:
- σ (entropia): {sigma:.3f}
- S (sintropia): {S:.3f}
- X (saldo): {X:.3f}

Interpretação: {x_interpretation}

Vetor de energia (10 dimensões, valores de 0 a 1):
{energy_formatted}

=== CONTEXTO DA CONVERSA ===
Pergunta raiz (objetivo principal):
\"\"\"{root_q}\"\"\"

Histórico recente:
{history_formatted}

=== MENSAGEM ATUAL DO USUÁRIO ===
\"\"\"{message}\"\"\"

=== INSTRUÇÕES DE RESPOSTA ===
1. Responda diretamente à pergunta do usuário.
2. Quando a pergunta envolver Modelo X / σ / S / X / entropia / sintropia:
   - Use explicitamente as definições do CONHECIMENTO_OFICIAL_MODELO_X acima.
   - Explique qualitativamente o que significa o estado atual de σ, S, X.
   - Sugira ações práticas (clarear requisitos, explorar hipóteses, reduzir escopo, etc.).
3. Mantenha o foco em engenharia de software.
4. Estruture a resposta com listas/passos quando isso ajudar a clareza.
5. Evite jargão matemático excessivo, a não ser que o usuário peça.
6. Se estiver corrigindo código, preserve o comportamento original exceto onde o bug é corrigido.
7. Se estiver refatorando, reduza complexidade sem mudar comportamento visível.
8. Permaneça alinhado com a pergunta raiz da conversa.

=== FORMATO DA RESPOSTA ===
- Se aplicável, inclua blocos de código com a linguagem especificada.
- Explique o raciocínio de forma clara e didática.
- Use markdown para formatação quando apropriado.
"""
    return prompt
