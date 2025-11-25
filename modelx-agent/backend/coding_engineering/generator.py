from typing import Dict, Any, Optional
import time
import logging
import os
from .prompts import build_main_prompt

# ============================================================================
# CONFIGURAÇÃO DO OLLAMA
# ============================================================================

# Nome do modelo a ser usado. Pode ser alterado para outros modelos disponíveis no Ollama.
# Exemplos: "llama3", "llama3:8b", "phi3", "mistral", "codellama", "qwen2", etc.
# Pode ser sobrescrito pela variável de ambiente OLLAMA_MODEL
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

# URL base do Ollama. Pode ser alterada para apontar para um servidor remoto.
# Pode ser sobrescrita pela variável de ambiente OLLAMA_URL
OLLAMA_BASE_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_GENERATE_ENDPOINT = f"{OLLAMA_BASE_URL}/api/generate"

# ============================================================================
# PARÂMETROS DE GERAÇÃO
# ============================================================================

# Limite máximo de caracteres do prompt (para evitar problemas com modelos menores)
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "12000"))

# Timeout para chamadas ao Ollama (em segundos)
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# Temperatura: controla a aleatoriedade das respostas
# - 0.0 a 0.3: respostas mais determinísticas e focadas
# - 0.7 a 1.0: respostas mais criativas e variadas
# Para o Model X Agent, usamos temperatura baixa para respostas consistentes
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.3"))

# Top-p (nucleus sampling): controla a diversidade
# - 0.1: apenas tokens mais prováveis
# - 0.9: considera mais opções
OLLAMA_TOP_P = float(os.getenv("OLLAMA_TOP_P", "0.9"))

# Top-k: número de tokens a considerar em cada passo
OLLAMA_TOP_K = int(os.getenv("OLLAMA_TOP_K", "40"))

# Número máximo de tokens na resposta
OLLAMA_NUM_PREDICT = int(os.getenv("OLLAMA_NUM_PREDICT", "2048"))

# Repeat penalty: penaliza repetições
OLLAMA_REPEAT_PENALTY = float(os.getenv("OLLAMA_REPEAT_PENALTY", "1.1"))

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _build_generation_options() -> Dict[str, Any]:
    """Constrói as opções de geração para o Ollama."""
    return {
        "temperature": OLLAMA_TEMPERATURE,
        "top_p": OLLAMA_TOP_P,
        "top_k": OLLAMA_TOP_K,
        "num_predict": OLLAMA_NUM_PREDICT,
        "repeat_penalty": OLLAMA_REPEAT_PENALTY,
    }


def call_llm(prompt: str, options: Optional[Dict[str, Any]] = None) -> str:
    """
    Chama o modelo local via Ollama.
    
    Args:
        prompt: O prompt a ser enviado para o modelo.
        options: Opções adicionais de geração (opcional).
    
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
        # Calcula o tamanho de cada parte considerando o texto de truncamento
        truncation_text = "\n\n[... conteúdo truncado ...]\n\n"
        available_length = MAX_PROMPT_LENGTH - len(truncation_text)
        half_length = available_length // 2
        
        # Monta o prompt truncado garantindo que não exceda o limite
        prompt = prompt[:half_length] + truncation_text + prompt[-half_length:]
        logger.warning(
            f"Prompt truncado de {original_length} para {len(prompt)} caracteres"
        )
    
    # Usa opções padrão se não fornecidas
    gen_options = options or _build_generation_options()
    
    logger.info(
        f"Chamando Ollama ({OLLAMA_MODEL_NAME}) - "
        f"Prompt: {len(prompt)} chars, "
        f"Temp: {gen_options.get('temperature', OLLAMA_TEMPERATURE)}"
    )
    
    start_time = time.time()
    
    try:
        request_body = {
            "model": OLLAMA_MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": gen_options
        }
        
        response = requests.post(
            OLLAMA_GENERATE_ENDPOINT,
            json=request_body,
            timeout=OLLAMA_TIMEOUT
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get("response", "")
            
            # Log de métricas (com proteção completa contra divisão por zero)
            eval_count = result.get("eval_count", 0)
            eval_duration = result.get("eval_duration", 0)
            
            if eval_count > 0 and eval_duration > 0:
                tokens_per_second = eval_count / (eval_duration / 1e9)
            else:
                tokens_per_second = 0.0
            
            logger.info(
                f"Resposta em {elapsed_time:.2f}s - "
                f"Tokens: {eval_count}, "
                f"Velocidade: {tokens_per_second:.1f} tok/s - "
                f"Preview: {answer[:80]}..."
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
            f"Dica: Você pode configurar a URL do Ollama com a variável de ambiente OLLAMA_URL.\n\n"
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
            f"Dica: Você pode aumentar o timeout com a variável de ambiente OLLAMA_TIMEOUT.\n\n"
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
                    state,
                    options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Gera uma resposta usando o Model X Agent.
    
    Args:
        message: Mensagem do usuário.
        energy_vector: Vetor de energia em 10 dimensões.
        sigma_S_X: Dicionário com valores de sigma, S e X.
        state: Estado da conversa.
        options: Opções adicionais de geração (opcional).
    
    Returns:
        Dicionário com a resposta e métricas do Modelo X.
    """
    prompt = build_main_prompt(message, state, energy_vector, sigma_S_X)
    raw_answer = call_llm(prompt, options)

    return {
        "answer_text": raw_answer,
        "energy_vector": energy_vector,
        "sigma": sigma_S_X["sigma"],
        "S": sigma_S_X["S"],
        "X": sigma_S_X["X"]
    }


def get_model_info() -> Dict[str, Any]:
    """
    Retorna informações sobre a configuração atual do modelo.
    
    Returns:
        Dicionário com informações de configuração.
    """
    return {
        "model_name": OLLAMA_MODEL_NAME,
        "base_url": OLLAMA_BASE_URL,
        "max_prompt_length": MAX_PROMPT_LENGTH,
        "timeout": OLLAMA_TIMEOUT,
        "generation_options": _build_generation_options()
    }
