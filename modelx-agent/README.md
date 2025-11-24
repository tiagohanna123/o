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

## Arquitetura

O Model X Agent é composto por duas partes independentes:

```
┌─────────────────────────────────────────────────────────────────┐
│                        ARQUITETURA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────┐         ┌─────────────────────────┐       │
│   │    FRONTEND     │  HTTP   │        BACKEND          │       │
│   │  (Estático)     │◄───────►│       (FastAPI)         │       │
│   │                 │  JSON   │                         │       │
│   │  - HTML/CSS/JS  │         │  - POST /chat           │       │
│   │  - Chat UI      │         │  - Modelo X             │       │
│   │  - Painel X     │         │  - Energia 10D          │       │
│   └─────────────────┘         └─────────────────────────┘       │
│          │                              │                        │
│          ▼                              ▼                        │
│   ┌─────────────────┐         ┌─────────────────────────┐       │
│   │ Netlify/Vercel  │         │ Railway/Render/VPS      │       │
│   │ GitHub Pages    │         │ Heroku/DigitalOcean     │       │
│   │ WordPress/iframe│         │ AWS/GCP/Azure           │       │
│   └─────────────────┘         └─────────────────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

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
    index.html          # Frontend estático completo
  requirements.txt
  README.md
```

---

## 🚀 Guia de Instalação e Deploy

### Pré-requisitos

- Python 3.8+
- pip

### 1. Instalação Local (Desenvolvimento)

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/tiagohanna123/o.git
cd o/modelx-agent

# Instale as dependências
pip install -r requirements.txt
```

### 2. Executar o Backend Localmente

```bash
cd modelx-agent
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em `http://127.0.0.1:8000`

### 3. Acessar o Frontend Localmente

Abra `frontend/index.html` diretamente no navegador ou sirva via:

```bash
# Opção 1: Python HTTP Server
cd frontend
python -m http.server 3000

# Opção 2: Se tiver Node.js
npx serve frontend -l 3000
```

Acesse `http://localhost:3000` e configure a URL da API nas configurações para `http://localhost:8000`.

---

## 🌐 Deploy em Produção

### Backend (FastAPI)

#### Opção A: Railway (Recomendado - Gratuito)

1. Crie uma conta em [railway.app](https://railway.app)
2. Conecte seu repositório GitHub
3. Configure:
   - **Root Directory**: `modelx-agent`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Adicione variável de ambiente se necessário
5. Deploy automático! URL será algo como: `https://seu-projeto.up.railway.app`

#### Opção B: Render (Gratuito)

1. Crie uma conta em [render.com](https://render.com)
2. New → Web Service → Conecte o repo
3. Configure:
   - **Root Directory**: `modelx-agent`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. URL: `https://seu-projeto.onrender.com`

#### Opção C: VPS/Servidor Próprio

```bash
# No servidor
cd modelx-agent
pip install -r requirements.txt

# Com gunicorn (produção)
pip install gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Configure reverse proxy (nginx) para HTTPS
```

**Exemplo de nginx config:**
```nginx
server {
    listen 443 ssl;
    server_name api.seudominio.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend (Estático)

#### Opção A: GitHub Pages (Gratuito)

1. Copie `frontend/index.html` para uma branch `gh-pages`
2. Configure nas Settings do repo → Pages
3. URL: `https://seuusuario.github.io/seu-repo/`

#### Opção B: Netlify (Recomendado - Gratuito)

1. Crie conta em [netlify.com](https://netlify.com)
2. Arraste a pasta `frontend` para o dashboard
3. URL automática: `https://nome-aleatorio.netlify.app`
4. Opcional: Configure domínio customizado

#### Opção C: Vercel (Gratuito)

1. Instale Vercel CLI: `npm i -g vercel`
2. Na pasta `frontend`: `vercel`
3. URL: `https://seu-projeto.vercel.app`

---

## 📝 Configuração da URL da API no Frontend

O frontend permite configurar a URL do backend de três formas:

### 1. Via Interface (Recomendado)

1. Abra o frontend no navegador
2. Clique em "⚙️ Configurações da API" no painel lateral
3. Digite a URL do seu backend (ex: `https://meu-backend.railway.app`)
4. A configuração é salva no localStorage do navegador

### 2. Via Código (Para Distribuição)

Edite o arquivo `frontend/index.html` e altere a linha:

```javascript
// Encontre esta linha no script:
const DEFAULT_API_URL = '';

// Altere para sua URL de produção:
const DEFAULT_API_URL = 'https://seu-backend.railway.app';
```

### 3. Mesma Origem (Desenvolvimento)

Se o frontend e backend estiverem no mesmo servidor, deixe a URL vazia e o frontend usará a mesma origem automaticamente.

---

## 🔌 Integração com WordPress/Elementor

### Método 1: iFrame (Mais Simples)

1. No Elementor, adicione um widget **HTML**
2. Cole o código:

```html
<iframe 
  src="https://seu-frontend.netlify.app" 
  width="100%" 
  height="700px" 
  style="border: none; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"
  allow="clipboard-read; clipboard-write"
></iframe>
```

3. Ajuste `src` para a URL do seu frontend hospedado
4. Ajuste `height` conforme necessário

### Método 2: Código Embutido Direto

Se preferir ter o chat diretamente na página (sem iframe):

1. No Elementor, adicione um widget **HTML**
2. Copie todo o conteúdo de `frontend/index.html`
3. Cole no widget HTML
4. **IMPORTANTE**: Altere a `DEFAULT_API_URL` no código para a URL do seu backend

**Vantagens do iframe:**
- Isolamento de CSS (não conflita com o tema WordPress)
- Fácil de atualizar (só muda o fonte)
- Melhor performance

**Vantagens do código embutido:**
- Mais controle sobre customização
- Sem requisição extra para carregar iframe
- Pode acessar o DOM pai se necessário

### Método 3: Subdomínio Dedicado

1. Configure um subdomínio no HostGator (ex: `chat.seudominio.com`)
2. Aponte para o frontend hospedado ou faça upload do `index.html`
3. Use iframe ou redirecione usuários para esse subdomínio

---

## 🔒 Configuração de CORS no Backend

Se o frontend estiver em um domínio diferente do backend, configure CORS no FastAPI.

Adicione no arquivo `backend/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Adicione após criar o app
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://seu-frontend.netlify.app",
        "https://seudominio.com",
        "http://localhost:3000",  # desenvolvimento
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Ou para permitir qualquer origem (menos seguro, apenas para testes):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 API

### POST /chat

**Request:**
```json
{
  "conversation_id": "string",
  "message": "string",
  "is_new_conversation": true
}
```

**Response:**
```json
{
  "answer_text": "string",
  "sigma": 0.0,
  "S": 0.0,
  "X": 0.0,
  "x_interpretation": "string",
  "energy_vector": {
    "syntax": 0.0,
    "semantic": 0.0,
    "pragmatic": 0.0,
    "computational": 0.0,
    "epistemic": 0.0,
    "structural": 0.0,
    "dynamic": 0.0,
    "social": 0.0,
    "creative": 0.0,
    "normative": 0.0
  },
  "coherence_score": 0.0
}
```

---

## 📐 Dimensões do Modelo de Energia

| # | Dimensão | Descrição |
|---|----------|-----------|
| 1 | **syntax** | Aspectos sintáticos |
| 2 | **semantic** | Aspectos semânticos |
| 3 | **pragmatic** | Aspectos pragmáticos |
| 4 | **computational** | Aspectos computacionais |
| 5 | **epistemic** | Aspectos epistêmicos |
| 6 | **structural** | Aspectos estruturais |
| 7 | **dynamic** | Aspectos dinâmicos |
| 8 | **social** | Aspectos sociais |
| 9 | **creative** | Aspectos criativos |
| 10 | **normative** | Aspectos normativos |

---

## 🔧 Pontos de Integração (TODO)

### Provedor de LLM Real
- Arquivo: `backend/coding_engineering/generator.py`
- Função: `call_llm(prompt: str)`
- TODO: integrar com OpenAI, Anthropic, ou outro provedor de LLM

### Compilação/Execução de Código
- Arquivo: `backend/coding_engineering/coherence_evaluator.py`
- Função: `run_static_checks_and_tests(answer)`
- TODO: integrar com ferramentas de compilação, linting e execução

### Embeddings
- Arquivo: `backend/main.py`
- Campo: `root_question_vector` em `ConversationState`
- TODO: calcular embeddings para comparação semântica

### Self-Critique via LLM
- Arquivo: `backend/coding_engineering/coherence_evaluator.py`
- Função: `answer_root_alignment_score()`
- TODO: usar LLM para comparar resposta à pergunta raiz

---

## 📋 Checklist de Deploy

- [ ] Backend funcionando localmente
- [ ] Backend hospedado com HTTPS
- [ ] CORS configurado no backend
- [ ] Frontend hospedado (Netlify/Vercel/GitHub Pages)
- [ ] URL da API configurada no frontend
- [ ] Testado envio de mensagens
- [ ] Métricas (σ, S, X) exibindo corretamente
- [ ] Integrado com WordPress/Elementor (se aplicável)

---

## 🆘 Troubleshooting

### "Erro ao enviar mensagem"
- Verifique se o backend está rodando
- Verifique se a URL da API está correta
- Verifique o console do navegador (F12) para erros CORS
- Configure CORS no backend se necessário

### Métricas não aparecem
- Verifique se a resposta da API contém `sigma`, `S`, `X`, `energy_vector`
- Verifique o console do navegador para erros JavaScript

### iframe não carrega no WordPress
- Certifique-se que o frontend está hospedado com HTTPS
- Alguns temas podem bloquear iframes - tente modo de edição limpo

---

## 📄 Licença

MIT
