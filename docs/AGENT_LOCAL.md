# Guia de Uso Local do Model X Agent com Ollama

Este guia explica como rodar o Model X Agent localmente usando o Ollama como backend de LLM.

---

## Requisitos

### Software necessário

- **Python 3.8+** (recomendado: 3.10 ou superior)
- **Ollama** instalado e funcionando
- **pip** para gerenciamento de pacotes

### Verificando a versão do Python

```bash
python --version
# ou
python3 --version
```

---

## 1. Instalação do Ollama

### Linux/macOS

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Windows

Baixe o instalador em: https://ollama.ai/download

### Verificando a instalação

```bash
ollama --version
```

---

## 2. Baixando um modelo

O Model X Agent usa o modelo `llama3` por padrão. Para baixá-lo:

```bash
ollama pull llama3
```

**Modelos alternativos recomendados:**

| Modelo | Comando | Descrição |
|--------|---------|-----------|
| LLaMA 3 8B | `ollama pull llama3:8b` | Bom equilíbrio entre qualidade e velocidade |
| Phi-3 | `ollama pull phi3` | Modelo menor e mais rápido |
| Mistral | `ollama pull mistral` | Alternativa eficiente |
| CodeLlama | `ollama pull codellama` | Especializado em código |

Para usar um modelo diferente, edite a constante `OLLAMA_MODEL_NAME` em:
`backend/coding_engineering/generator.py`

---

## 3. Configurando o ambiente Python

### Clone o repositório (se ainda não tiver)

```bash
git clone https://github.com/tiagohanna123/o.git
cd o
```

### Crie e ative o ambiente virtual

**Linux/macOS:**
```bash
cd modelx-agent
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
cd modelx-agent
python -m venv venv
.\venv\Scripts\activate
```

### Instale as dependências

```bash
pip install -r requirements.txt
```

Isso instalará:
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `pydantic` - Validação de dados
- `requests` - Cliente HTTP para chamar o Ollama

---

## 4. Executando o agente

### Terminal 1: Inicie o Ollama

```bash
ollama serve
```

O Ollama estará disponível em `http://127.0.0.1:11434`

### Terminal 2: Inicie o backend

```bash
cd modelx-agent
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

O servidor estará disponível em `http://127.0.0.1:8000`

### Acesse o frontend

Abra `http://127.0.0.1:8000` no navegador.

Ou, se preferir servir o frontend separadamente:

```bash
cd frontend
python -m http.server 3000
```

E acesse `http://localhost:3000`

---

## 5. Testando o agente

### Via navegador

1. Acesse `http://127.0.0.1:8000`
2. Digite uma mensagem no chat
3. Observe as métricas do Modelo X (σ, S, X) no painel

### Via API (curl)

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-1",
    "message": "Explique o que é o Modelo X (X = σ − S) em linguagem simples.",
    "is_new_conversation": true
  }'
```

### Via Python

```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={
        "conversation_id": "test-1",
        "message": "Explique o que é o Modelo X",
        "is_new_conversation": True
    }
)

data = response.json()
print(f"Resposta: {data['answer_text']}")
print(f"σ = {data['sigma']:.3f}")
print(f"S = {data['S']:.3f}")
print(f"X = {data['X']:.3f}")
```

---

## 6. Exemplos de prompts em português

### Perguntas sobre o Modelo X

```text
"Explique o que é o Modelo X (X = σ − S) em linguagem simples."

"Com base nos valores atuais de σ, S e X, o que isso diz sobre o estado da minha sessão de trabalho?"

"Dê um exemplo de situação de debugging com X muito positivo e outra com X muito negativo."

"Qual a diferença entre entropia (σ) e sintropia (S) no contexto do Modelo X?"

"Como posso reduzir o X quando estou em um cenário de debug caótico?"
```

### Perguntas de engenharia de software

```text
"Como refatorar uma função com muitos if-else aninhados?"

"Quais são as melhores práticas para testes unitários em Python?"

"Explique o padrão de design Strategy com um exemplo em código."

"Como estruturar um plano de sprint para uma equipe de 5 desenvolvedores?"
```

---

## 7. Solução de problemas

### Erro: "Não foi possível conectar ao Ollama"

**Causa:** O Ollama não está em execução.

**Solução:**
```bash
ollama serve
```

### Erro: "Modelo não encontrado"

**Causa:** O modelo não foi baixado.

**Solução:**
```bash
ollama pull llama3
```

### Timeout na resposta

**Causa:** O modelo está demorando para responder (comum na primeira execução).

**Soluções:**
1. Aguarde mais tempo (a primeira resposta pode demorar)
2. Use um modelo menor: `ollama pull phi3`
3. Aumente o timeout em `generator.py`: `OLLAMA_TIMEOUT = 120`

### Resposta truncada ou incompleta

**Causa:** Prompt muito longo para o modelo.

**Solução:** O sistema trunca automaticamente prompts muito longos. Se isso acontecer frequentemente, considere:
- Reduzir o histórico de conversa
- Usar um modelo com contexto maior

---

## 8. Configuração avançada

### Alterando o modelo

Edite `backend/coding_engineering/generator.py`:

```python
OLLAMA_MODEL_NAME = "phi3"  # ou outro modelo
```

### Alterando o timeout

```python
OLLAMA_TIMEOUT = 120  # segundos
```

### Alterando o limite de prompt

```python
MAX_PROMPT_LENGTH = 12000  # caracteres
```

### Usando um servidor Ollama remoto

```python
OLLAMA_BASE_URL = "http://192.168.1.100:11434"
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"
```

---

## 9. Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA LOCAL                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────┐         ┌─────────────────────────┐       │
│   │    FRONTEND     │  HTTP   │        BACKEND          │       │
│   │  (Estático)     │◄───────►│       (FastAPI)         │       │
│   │  localhost:3000 │  JSON   │    localhost:8000       │       │
│   │  ou :8000       │         │                         │       │
│   └─────────────────┘         └───────────┬─────────────┘       │
│                                           │                      │
│                                           │ HTTP (JSON)          │
│                                           ▼                      │
│                               ┌─────────────────────────┐       │
│                               │        OLLAMA           │       │
│                               │    localhost:11434      │       │
│                               │                         │       │
│                               │  Modelos: llama3, etc.  │       │
│                               └─────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Próximos passos

1. **Experimente diferentes modelos** para encontrar o melhor equilíbrio entre qualidade e velocidade.
2. **Customize os prompts** em `backend/coding_engineering/prompts.py` para seu caso de uso.
3. **Leia a documentação do Modelo X** em `docs/modelo_x.md` para entender melhor os conceitos.
4. **Contribua** com melhorias via pull requests!

---

## Referências

- [Ollama - Documentação oficial](https://ollama.ai/docs)
- [FastAPI - Documentação](https://fastapi.tiangolo.com/)
- [Modelo X - Conhecimento oficial](../docs/modelo_x.md)
