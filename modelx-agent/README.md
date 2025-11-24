# ModelX Agent

Assistente de engenharia de software baseado no Modelo X (X = σ − S).

## Características

- **Modelo decadimensional de energia** (10 dimensões)
- **Cálculo de σ (entropia), S (sintropia) e X = σ − S**
- **Ajuste dinâmico de energia** com base:
  - no domínio `coding_engineering`
  - no ritmo/tempo do usuário (latência, tamanho das mensagens)
  - na coerência das respostas
- **Ciclo de autoajuste**:
  - avalia coerência técnica (compila, testes, etc. – inicialmente stubs)
  - avalia alinhamento com a pergunta raiz da conversa
  - atualiza pesos de energia e pesos entropia/sintropia

## Estrutura do Projeto

```
modelx-agent/
  backend/
    __init__.py
    main.py
    conversation_state.py
    domains.py
    energy_model.py
    modelx_core.py
    meta_learning.py
    coding_engineering/
      __init__.py
      interpret.py
      prompts.py
      generator.py
      coherence_evaluator.py
  frontend/
    index.html
  requirements.txt
  README.md
```

## Instalação

```bash
cd modelx-agent
pip install -r requirements.txt
```

## Execução

```bash
uvicorn backend.main:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

## Pontos de Integração

### Provedor de LLM Real
- Arquivo: `backend/coding_engineering/generator.py`
- Função: `call_llm(prompt: str)`
- TODO: integrar com OpenAI, Anthropic, ou outro provedor de LLM

### Compilação/Execução de Código
- Arquivo: `backend/coding_engineering/coherence_evaluator.py`
- Função: `run_static_checks_and_tests(answer)`
- TODO: integrar com ferramentas de compilação, linting e execução

### Testes Automáticos
- Arquivo: `backend/coding_engineering/coherence_evaluator.py`
- Função: `run_static_checks_and_tests(answer)`
- TODO: integrar com pytest, unittest ou framework de testes

### Embeddings
- Arquivo: `backend/main.py`
- Campo: `root_question_vector` em `ConversationState`
- TODO: calcular embeddings para comparação semântica

### Self-Critique via LLM
- Arquivo: `backend/coding_engineering/coherence_evaluator.py`
- Função: `answer_root_alignment_score()`
- TODO: usar LLM para comparar resposta à pergunta raiz

## API

### POST /chat

Request:
```json
{
  "conversation_id": "string",
  "message": "string",
  "is_new_conversation": true
}
```

Response:
```json
{
  "answer_text": "string",
  "sigma": 0.0,
  "S": 0.0,
  "X": 0.0,
  "x_interpretation": "string",
  "energy_vector": {},
  "coherence_score": 0.0
}
```

## Dimensões do Modelo de Energia

1. **syntax** - Aspectos sintáticos
2. **semantic** - Aspectos semânticos
3. **pragmatic** - Aspectos pragmáticos
4. **computational** - Aspectos computacionais
5. **epistemic** - Aspectos epistêmicos
6. **structural** - Aspectos estruturais
7. **dynamic** - Aspectos dinâmicos
8. **social** - Aspectos sociais
9. **creative** - Aspectos criativos
10. **normative** - Aspectos normativos

## Licença

MIT
