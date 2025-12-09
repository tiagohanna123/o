# Model X AI Reasoning System

Sistema de Inteligencia Artificial que usa o **Model X** como logica de reasoning base, integrado com **LLMs open source gratuitos**.

## Arquitetura

```
                    +------------------+
                    |   User Request   |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |   Model X Core   |
                    |  (σ, S, X = σ-S) |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
              v              v              v
      +-------+------+ +-----+------+ +-----+------+
      | Reasoning    | | Chain of   | | Reflective |
      | Engine       | | Thought    | | Reasoner   |
      +--------------+ +------------+ +------------+
              |              |              |
              +--------------+--------------+
                             |
                             v
                    +------------------+
                    | Unified LLM      |
                    | Provider         |
                    +--------+---------+
                             |
        +----------+---------+---------+----------+
        |          |         |         |          |
        v          v         v         v          v
    +------+  +--------+  +------+  +--------+  +----+
    |Ollama|  |Hugging |  | Groq |  |Together|  |... |
    |(local)|  | Face   |  |(fast)|  |  .ai   |  |    |
    +------+  +--------+  +------+  +--------+  +----+
```

## Componentes Principais

### 1. LLM Providers (`llm_providers.py`)

Interface unificada para multiplos LLMs gratuitos:

| Provider | Tipo | Velocidade | Modelos Recomendados |
|----------|------|------------|----------------------|
| **Ollama** | Local | Media | llama3:8b, mistral:7b, codellama:13b |
| **Groq** | Cloud | Muito Rapida | llama-3.1-8b-instant, mixtral-8x7b |
| **Hugging Face** | Cloud | Media | Mistral-7B-Instruct, Phi-3-mini |
| **Together.ai** | Cloud | Rapida | Llama-3.2-3B-Instruct-Turbo |

### 2. Reasoning Engine (`reasoning_engine.py`)

Motor de reasoning que usa o Model X para guiar decisoes:

```python
from modelx_agent.backend.reasoning_engine import reason

result = reason(
    question="Como otimizar queries SQL lentas?",
    sigma=0.6,  # entropia (caos)
    S=0.3,      # sintropia (ordem)
    X=0.3,      # saldo de entropia
    energy_vector={...}
)

print(result.answer)
print(f"Estrategia: {result.strategy_used}")
print(f"Confianca: {result.confidence}")
```

**Estrategias automaticas:**
- `STRUCTURING`: X alto → foca em estrutura e clareza
- `EXPLORING`: X baixo → explora alternativas
- `BALANCED`: X equilibrado → abordagem balanceada
- `DEEP_ANALYSIS`: Problemas complexos
- `QUICK_RESPONSE`: Queries simples

### 3. Chain of Thought (`chain_of_thought.py`)

Raciocinio estruturado em etapas:

```python
from modelx_agent.backend.chain_of_thought import think

result = think(
    question="Explique o Model X",
    initial_x=0.2,
    chain_type="default"  # ou "short"
)

for thought in result.thoughts:
    print(f"[{thought.type}] {thought.content[:100]}...")

print(f"\nResposta: {result.final_answer}")
```

**Tipos de pensamento:**
- OBSERVE → ANALYZE → HYPOTHESIZE → REFLECT → VERIFY → CONCLUDE → CRITIQUE

### 4. Reflective Reasoner

Raciocinio iterativo com auto-reflexao:

```python
from modelx_agent.backend.chain_of_thought import reflect_and_reason

result = reflect_and_reason(
    question="Como implementar autenticacao JWT?",
    sigma=0.5,
    S=0.5
)

print(f"Resposta final: {result['final_answer']}")
print(f"Iteracoes: {result['total_iterations']}")
print(f"Convergiu: {result['converged']}")
```

## Configuracao

### Variaveis de Ambiente

```bash
# Modo de geracao
export GENERATION_MODE=reasoning  # simple, reasoning, chain, reflective

# Provedor preferido
export PREFERRED_PROVIDER=auto    # auto, ollama, groq, huggingface, together

# Ollama (local)
export OLLAMA_MODEL=llama3
export OLLAMA_URL=http://127.0.0.1:11434

# Groq (cloud, muito rapido)
export GROQ_API_KEY=sua_key_aqui
export GROQ_MODEL=llama-3.1-8b-instant

# Hugging Face
export HF_TOKEN=seu_token_aqui
export HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3

# Together.ai
export TOGETHER_API_KEY=sua_key_aqui
export TOGETHER_MODEL=meta-llama/Llama-3.2-3B-Instruct-Turbo

# Opcoes avancadas
export ENABLE_FULL_CHAIN=false    # Chain completo (mais lento)
export ENABLE_REFLECTION=false    # Reflexao iterativa
```

### Instalacao

```bash
# 1. Dependencias
cd modelx-agent
pip install -r requirements.txt

# 2. Ollama (recomendado para desenvolvimento)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
ollama serve  # Em outro terminal

# 3. Rodar o servidor
uvicorn backend.main:app --reload --port 8000
```

## Uso via API

### Endpoint `/chat`

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-1",
    "message": "Explique o que e entropia no Model X",
    "is_new_conversation": true
  }'
```

**Resposta:**
```json
{
  "answer_text": "No Model X, entropia (σ) representa...",
  "sigma": 0.45,
  "S": 0.55,
  "X": -0.10,
  "x_interpretation": "Estado: EQUILIBRIO SAUDAVEL...",
  "energy_vector": {...},
  "coherence_score": 0.85
}
```

## Como o Model X Guia o Reasoning

### 1. Selecao de Estrategia

O valor de X (σ - S) determina a abordagem:

```
X > 0.3  (muito caos)    → STRUCTURING: força estrutura
X < -0.3 (muita ordem)   → EXPLORING: incentiva flexibilidade
-0.3 ≤ X ≤ 0.3          → BALANCED: equilibrio natural
```

### 2. Ajuste Dinamico

Durante o reasoning, X e ajustado baseado em:
- Tipo de pensamento atual
- Confianca das respostas anteriores
- Posicao na cadeia de pensamento

### 3. Auto-Reflexao

O sistema avalia suas proprias respostas:
- Completude (cobre todos aspectos?)
- Clareza (facil de entender?)
- Precisao (informacoes corretas?)
- Praticidade (util e aplicavel?)

## Modelos Recomendados por Caso de Uso

| Caso de Uso | Provedor | Modelo |
|-------------|----------|--------|
| **Desenvolvimento** | Ollama | llama3:8b |
| **Producao (rapido)** | Groq | llama-3.1-8b-instant |
| **Codigo** | Ollama | codellama:13b |
| **Multilingue** | Ollama | qwen2:7b |
| **Baixo recurso** | Ollama | phi3:mini |

## Extensibilidade

### Adicionar Novo Provedor

```python
from modelx_agent.backend.llm_providers import BaseLLMProvider, LLMProvider

class MeuProvedor(BaseLLMProvider):
    @property
    def provider_type(self) -> LLMProvider:
        return LLMProvider.MEU_PROVEDOR

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, config=None) -> LLMResponse:
        # Implementar chamada a API
        pass
```

### Personalizar Estrategia de Reasoning

```python
from modelx_agent.backend.reasoning_engine import ModelXReasoningEngine

engine = ModelXReasoningEngine()

# Sobrescrever thresholds
engine.HIGH_ENTROPY_THRESHOLD = 0.4
engine.LOW_ENTROPY_THRESHOLD = -0.4

# Adicionar estrategia custom
engine.STRATEGY_PROMPTS[ReasoningStrategy.CUSTOM] = "..."
```

## Metricas e Observabilidade

```python
from modelx_agent.backend.llm_providers import get_default_provider

provider = get_default_provider()
metrics = provider.get_metrics()

print(f"Total requests: {metrics['total_requests']}")
print(f"Sucesso: {metrics['successful_requests']}")
print(f"Tokens usados: {metrics['total_tokens']}")
print(f"Latencia media: {metrics['avg_latency_ms']:.0f}ms")
```

## Troubleshooting

### Ollama nao conecta
```bash
# Verificar se esta rodando
curl http://localhost:11434/api/tags

# Reiniciar
pkill ollama
ollama serve
```

### Rate limit no Hugging Face
- Use Ollama para desenvolvimento
- Ou obtenha Pro account no HF

### Respostas lentas
- Use Groq (mais rapido)
- Reduza `max_tokens`
- Use `GENERATION_MODE=simple`

## Licenca

MIT License - Veja LICENSE para detalhes.
