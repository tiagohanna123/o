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


# Exemplos de comportamento esperado (few-shot learning)
FEW_SHOT_EXAMPLES = """
=== EXEMPLOS DE COMPORTAMENTO CORRETO ===

**Exemplo 1: Pergunta sobre o Modelo X**
Usuário: "O que é σ no Modelo X?"
Resposta correta:
No Modelo X, σ (sigma) representa a **entropia** — ou seja, a medida de desordem, incerteza e caos no sistema.

Em termos práticos de engenharia de software:
- σ alto significa muita confusão: muitas hipóteses de bugs, requisitos indefinidos, código desorganizado.
- σ baixo significa menos incerteza: problema bem definido, causa conhecida, caminho claro.

A fórmula central é X = σ − S, onde S é a sintropia (ordem/estrutura).

**Exemplo 2: Interpretação do estado atual**
Usuário: "Com σ=0.7 e S=0.3, o que isso significa?"
Resposta correta:
Com σ = 0.7 e S = 0.3, temos X = σ − S = 0.4.

Isso indica um estado de **alta entropia**:
- Há muita incerteza/confusão na sua sessão de trabalho
- A estrutura/organização está abaixo do ideal

**Sugestões práticas:**
1. Liste os problemas/hipóteses e priorize os mais prováveis
2. Clarifique os requisitos ou o objetivo principal
3. Reduza o escopo temporariamente para ganhar clareza
4. Divida o problema em partes menores

**Exemplo 3: INCORRETO (nunca fazer)**
Usuário: "O que é σ no Modelo X?"
❌ Resposta INCORRETA: "σ representa a entropia sintática do código..."
❌ Resposta INCORRETA: "σ significa 'syntactic entropy'..."
❌ Resposta INCORRETA: "S significa 'semantic significance'..."

Estas interpretações estão ERRADAS. σ é sempre entropia/desordem/caos, e S é sempre sintropia/ordem/estrutura.
"""


def _format_energy_vector(energy_vector: Dict[str, float]) -> str:
    """Formata o vetor de energia de forma legível com descrições."""
    descriptions = {
        'syntax': 'sintaxe/estrutura do código',
        'semantic': 'significado/lógica',
        'pragmatic': 'uso prático/contexto',
        'computational': 'performance/complexidade',
        'epistemic': 'conhecimento/certeza',
        'structural': 'arquitetura/organização',
        'dynamic': 'mudança/evolução',
        'social': 'colaboração/comunicação',
        'creative': 'inovação/novidade',
        'normative': 'regras/boas práticas'
    }
    
    lines = []
    for key, value in energy_vector.items():
        desc = descriptions.get(key, key)
        # Adiciona indicador visual do nível
        level = "baixo" if value < 0.33 else "médio" if value < 0.67 else "alto"
        lines.append(f"  - {key} ({desc}): {value:.3f} [{level}]")
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
    """Gera uma interpretação qualitativa detalhada do estado de X."""
    # Determina o nível de entropia e sintropia
    sigma_level = "alta" if sigma > 0.6 else "média" if sigma > 0.3 else "baixa"
    s_level = "alta" if S > 0.6 else "média" if S > 0.3 else "baixa"
    
    if X > 0.5:
        estado = "ALTA ENTROPIA (muito caos)"
        descricao = "Há muita confusão, incerteza e dispersão. O sistema está desorganizado."
        sugestoes = "Clarifique requisitos, priorize hipóteses, reduza escopo."
    elif X > 0.2:
        estado = "ENTROPIA MODERADA"
        descricao = "Há alguma incerteza, mas ainda manejável. Bom momento para definir próximos passos."
        sugestoes = "Defina prioridades, documente decisões, mantenha foco."
    elif X > -0.2:
        estado = "EQUILÍBRIO SAUDÁVEL"
        descricao = "Balanço ideal entre exploração e estrutura. Sistema produtivo."
        sugestoes = "Mantenha o ritmo, monitore as métricas, ajuste conforme necessário."
    elif X > -0.5:
        estado = "SINTROPIA MODERADA"
        descricao = "Boa estrutura, mas pode haver pouca flexibilidade. Cuidado com rigidez."
        sugestoes = "Questione premissas ocasionalmente, mantenha abertura para mudanças."
    else:
        estado = "ALTA SINTROPIA (muita rigidez)"
        descricao = "Estrutura excessiva pode estar limitando adaptação e criatividade."
        sugestoes = "Simplifique abstrações, explore alternativas, aceite mais incerteza."
    
    return f"""Estado: {estado}
  - σ (entropia): {sigma:.3f} ({sigma_level})
  - S (sintropia): {S:.3f} ({s_level})
  - X (saldo): {X:.3f}
  
Descrição: {descricao}
Sugestão: {sugestoes}"""


def _detect_language(message: str) -> str:
    """Detecta o idioma da mensagem do usuário (heurística simples)."""
    # Palavras comuns em português
    pt_words = {'que', 'como', 'para', 'com', 'uma', 'um', 'não', 'por', 'mais', 'se', 
                'quando', 'qual', 'isso', 'este', 'esta', 'aqui', 'onde', 'fazer', 
                'você', 'eu', 'nós', 'ele', 'ela', 'eles', 'elas', 'código', 'função',
                'explique', 'ajude', 'preciso', 'quero', 'tenho', 'estou', 'está'}
    
    # Palavras comuns em inglês
    en_words = {'the', 'is', 'are', 'what', 'how', 'for', 'with', 'this', 'that', 
                'not', 'but', 'can', 'you', 'have', 'from', 'when', 'which', 'there',
                'code', 'function', 'explain', 'help', 'need', 'want', 'please'}
    
    words = set(message.lower().split())
    
    pt_count = len(words & pt_words)
    en_count = len(words & en_words)
    
    if en_count > pt_count:
        return "en"
    return "pt"


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
    detected_lang = _detect_language(message)
    
    # Determina o idioma de resposta
    if detected_lang == "en":
        lang_instruction = """- A mensagem do usuário parece estar em INGLÊS.
- Responda em INGLÊS se o usuário continuar em inglês.
- Se preferir, o usuário pode pedir para mudar para português a qualquer momento."""
    else:
        lang_instruction = """- Responda em **PORTUGUÊS** (idioma padrão).
- Só mude de idioma se o usuário pedir explicitamente."""

    prompt = f"""# Model X Agent — Assistente de Engenharia de Software

## IDENTIDADE
Você é o **Model X Agent**, um assistente de IA especializado em:
- Engenharia de software (debugging, refatoração, arquitetura, testes, sprints)
- Análise de sessões de trabalho usando o Modelo X (X = σ − S)

## IDIOMA
{lang_instruction}

## CONHECIMENTO OFICIAL DO MODELO X

⚠️ **IMPORTANTE**: Este é o conhecimento oficial. Siga estas definições EXATAMENTE.

<<<CONHECIMENTO_OFICIAL>>>
{MODELO_X_KNOWLEDGE}
<<<FIM_CONHECIMENTO>>>

## REGRAS ESTRITAS

### ✅ VOCÊ DEVE:
1. Usar SEMPRE a fórmula **X = σ − S** ao explicar o Modelo X
2. Definir σ (sigma) como **entropia/desordem/incerteza/caos**
3. Definir S como **sintropia/ordem/estrutura/organização**
4. Usar analogias práticas de engenharia de software
5. Sugerir ações concretas baseadas no valor de X
6. Seguir o documento de conhecimento oficial acima

### ❌ VOCÊ NÃO PODE:
1. Redefinir σ como "syntactic entropy", "syntax entropy" ou similar
2. Redefinir S como "semantic significance", "semantic entropy" ou similar
3. Inventar novas fórmulas para o Modelo X
4. Ignorar os valores atuais de σ, S e X
5. Usar jargão matemático excessivo sem explicação
6. Responder em inglês quando o usuário está em português

{FEW_SHOT_EXAMPLES}

## ESTADO ATUAL DA SESSÃO

### Modelo X
{x_interpretation}

### Vetor de Energia (10 dimensões)
{energy_formatted}

## CONTEXTO DA CONVERSA

### Pergunta/Objetivo Raiz
"{root_q}"

### Histórico Recente
{history_formatted}

## MENSAGEM DO USUÁRIO

"{message}"

## INSTRUÇÕES DE RESPOSTA

1. **Responda diretamente** à pergunta do usuário
2. Se a pergunta envolver Modelo X, σ, S, X, entropia ou sintropia:
   - Use as definições do CONHECIMENTO OFICIAL acima
   - Explique o estado atual (σ={sigma:.3f}, S={S:.3f}, X={X:.3f})
   - Sugira ações práticas
3. Mantenha foco em **engenharia de software**
4. Use **listas e passos** para clareza
5. Inclua **blocos de código** quando relevante
6. Permaneça **alinhado com a pergunta raiz**
7. Seja **didático** e evite jargão desnecessário

## SUA RESPOSTA

"""
    return prompt


def build_simple_prompt(message: str, sigma_S_X: Dict[str, float]) -> str:
    """
    Constrói um prompt simplificado para casos que não precisam do contexto completo.
    
    Args:
        message: Mensagem do usuário.
        sigma_S_X: Dicionário com valores de sigma, S e X.
    
    Returns:
        Prompt simplificado.
    """
    sigma = sigma_S_X["sigma"]
    S = sigma_S_X["S"]
    X = sigma_S_X["X"]
    
    return f"""Você é o Model X Agent, especialista em engenharia de software e no Modelo X.

Modelo X: X = σ − S
- σ (sigma) = entropia/desordem/caos
- S = sintropia/ordem/estrutura
- X = saldo de entropia

Estado atual: σ={sigma:.3f}, S={S:.3f}, X={X:.3f}

Responda em português:
"{message}"
"""
