from typing import Dict, Any
import time
import logging
from .prompts import build_main_prompt

# Configuração do Ollama
# Nome do modelo a ser usado. Pode ser alterado para outros modelos disponíveis no Ollama.
# Exemplos: "llama3", "llama3:8b", "phi3", "mistral", "codellama", etc.
OLLAMA_MODEL_NAME = "llama3"
OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# Limite máximo de caracteres do prompt (para evitar problemas com modelos menores)
MAX_PROMPT_LENGTH = 8000

# Timeout para chamadas ao Ollama (em segundos)
OLLAMA_TIMEOUT = 90

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def call_llm(prompt: str) -> str:
    """
    Chama o modelo local via Ollama.
    
    Args:
        prompt: O prompt a ser enviado para o modelo.
    
    Returns:
        A resposta do modelo ou uma mensagem de erro em português.
    """
    try:
        import requests
    except ImportError:
        return (
            "Erro: A biblioteca 'requests' não está instalada.\n"
            "Execute: pip install requests"
        )
    
    # Trunca o prompt se necessário
    original_length = len(prompt)
    if original_length > MAX_PROMPT_LENGTH:
        prompt = prompt[:MAX_PROMPT_LENGTH]
        logger.warning(
            f"Prompt truncado de {original_length} para {MAX_PROMPT_LENGTH} caracteres"
        )
    
    logger.info(f"Chamando Ollama ({OLLAMA_MODEL_NAME}) - Tamanho do prompt: {len(prompt)} chars")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            OLLAMA_GENERATE_ENDPOINT,
            json={
                "model": OLLAMA_MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=OLLAMA_TIMEOUT
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "")
            
            logger.info(
                f"Resposta recebida em {elapsed_time:.2f}s - "
                f"Primeiros 100 chars: {answer[:100]}..."
            )
            
            return answer
        else:
            error_msg = (
                f"Erro ao chamar o modelo local (Ollama).\n\n"
                f"Verifique se o Ollama está em execução e se o modelo \"{OLLAMA_MODEL_NAME}\" está disponível.\n\n"
                f"Para instalar o modelo, execute:\n"
                f"  ollama pull {OLLAMA_MODEL_NAME}\n\n"
                f"Detalhes técnicos:\n"
                f"  - Status HTTP: {response.status_code}\n"
                f"  - Resposta: {response.text[:200]}"
            )
            logger.error(error_msg)
            return error_msg
            
    except requests.exceptions.ConnectionError:
        error_msg = (
            f"Erro ao chamar o modelo local (Ollama).\n\n"
            f"Não foi possível conectar ao Ollama em {OLLAMA_BASE_URL}.\n\n"
            f"Verifique se o Ollama está em execução:\n"
            f"  1. Instale o Ollama: https://ollama.ai/download\n"
            f"  2. Execute: ollama serve\n"
            f"  3. Em outro terminal: ollama pull {OLLAMA_MODEL_NAME}\n\n"
            f"Detalhes técnicos: Conexão recusada"
        )
        logger.error(error_msg)
        return error_msg
        
    except requests.exceptions.Timeout:
        elapsed_time = time.time() - start_time
        error_msg = (
            f"Erro ao chamar o modelo local (Ollama).\n\n"
            f"A requisição excedeu o tempo limite de {OLLAMA_TIMEOUT} segundos.\n\n"
            f"Isso pode acontecer se:\n"
            f"  - O modelo está sendo carregado pela primeira vez (aguarde e tente novamente)\n"
            f"  - O prompt é muito longo\n"
            f"  - O hardware não tem recursos suficientes\n\n"
            f"Detalhes técnicos:\n"
            f"  - Tempo decorrido: {elapsed_time:.2f}s\n"
            f"  - Timeout configurado: {OLLAMA_TIMEOUT}s"
        )
        logger.error(error_msg)
        return error_msg
        
    except requests.exceptions.RequestException as e:
        error_msg = (
            f"Erro ao chamar o modelo local (Ollama).\n\n"
            f"Ocorreu um erro de rede inesperado.\n\n"
            f"Verifique se o Ollama está em execução e se o modelo \"{OLLAMA_MODEL_NAME}\" está disponível.\n\n"
            f"Detalhes técnicos: {str(e)}"
        )
        logger.error(error_msg)
        return error_msg


def generate_answer(message: str,
                    energy_vector: Dict[str, float],
                    sigma_S_X: Dict[str, float],
                    state) -> Dict[str, Any]:
    """
    Gera uma resposta usando o Model X Agent.
    
    Args:
        message: Mensagem do usuário.
        energy_vector: Vetor de energia em 10 dimensões.
        sigma_S_X: Dicionário com valores de sigma, S e X.
        state: Estado da conversa.
    
    Returns:
        Dicionário com a resposta e métricas do Modelo X.
    """
    prompt = build_main_prompt(message, state, energy_vector, sigma_S_X)
    raw_answer = call_llm(prompt)

    return {
        "answer_text": raw_answer,
        "energy_vector": energy_vector,
        "sigma": sigma_S_X["sigma"],
        "S": sigma_S_X["S"],
        "X": sigma_S_X["X"]
    }
