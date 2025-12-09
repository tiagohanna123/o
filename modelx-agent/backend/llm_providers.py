"""
LLM Providers - Suporte a múltiplos LLMs open source gratuitos.

Este módulo fornece uma interface unificada para diferentes provedores de LLM:
- Ollama (local, gratuito)
- Hugging Face Inference API (gratuito com rate limits)
- Groq (tier gratuito muito rápido)
- Together.ai (tier gratuito)

O Model X Agent usa estes provedores para gerar respostas, combinando
a lógica de reasoning do Model X com a capacidade generativa dos LLMs.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import os
import time
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    """Provedores de LLM disponíveis."""
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    GROQ = "groq"
    TOGETHER = "together"


@dataclass
class LLMResponse:
    """Resposta padronizada de um LLM."""
    text: str
    provider: LLMProvider
    model: str
    tokens_used: int = 0
    latency_ms: float = 0.0
    success: bool = True
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "provider": self.provider.value,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms,
            "success": self.success,
            "error_message": self.error_message
        }


@dataclass
class GenerationConfig:
    """Configuração para geração de texto."""
    temperature: float = 0.3
    max_tokens: int = 2048
    top_p: float = 0.9
    top_k: int = 40
    repeat_penalty: float = 1.1
    stop_sequences: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repeat_penalty": self.repeat_penalty,
            "stop_sequences": self.stop_sequences or []
        }


class BaseLLMProvider(ABC):
    """Classe base abstrata para provedores de LLM."""

    def __init__(self, model_name: str, config: Optional[GenerationConfig] = None):
        self.model_name = model_name
        self.config = config or GenerationConfig()

    @abstractmethod
    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> LLMResponse:
        """Gera texto a partir de um prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível."""
        pass

    @property
    @abstractmethod
    def provider_type(self) -> LLMProvider:
        """Retorna o tipo do provedor."""
        pass


class OllamaProvider(BaseLLMProvider):
    """
    Provedor Ollama para LLMs locais.

    Modelos recomendados (gratuitos, rodam localmente):
    - llama3:8b (recomendado para hardware moderado)
    - llama3:70b (para hardware potente)
    - mistral:7b (rápido e eficiente)
    - codellama:13b (especializado em código)
    - phi3:mini (muito leve, ~3GB RAM)
    - qwen2:7b (ótimo para múltiplos idiomas)

    Instalação:
    1. curl -fsSL https://ollama.ai/install.sh | sh
    2. ollama pull llama3:8b
    3. ollama serve
    """

    def __init__(
        self,
        model_name: str = None,
        base_url: str = None,
        config: Optional[GenerationConfig] = None
    ):
        model = model_name or os.getenv("OLLAMA_MODEL", "llama3")
        super().__init__(model, config)
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "120"))

    @property
    def provider_type(self) -> LLMProvider:
        return LLMProvider.OLLAMA

    def is_available(self) -> bool:
        try:
            import requests
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> LLMResponse:
        try:
            import requests
        except ImportError:
            return LLMResponse(
                text="Erro: biblioteca 'requests' não instalada",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="pip install requests"
            )

        cfg = config or self.config
        start_time = time.time()

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": cfg.temperature,
                        "top_p": cfg.top_p,
                        "top_k": cfg.top_k,
                        "num_predict": cfg.max_tokens,
                        "repeat_penalty": cfg.repeat_penalty
                    }
                },
                timeout=self.timeout
            )

            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                return LLMResponse(
                    text=result.get("response", ""),
                    provider=self.provider_type,
                    model=self.model_name,
                    tokens_used=result.get("eval_count", 0),
                    latency_ms=latency,
                    success=True
                )
            else:
                return LLMResponse(
                    text="",
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )

        except requests.exceptions.ConnectionError:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=f"Não foi possível conectar ao Ollama em {self.base_url}. Execute: ollama serve"
            )
        except requests.exceptions.Timeout:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=f"Timeout após {self.timeout}s"
            )
        except Exception as e:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=str(e)
            )


class HuggingFaceProvider(BaseLLMProvider):
    """
    Provedor Hugging Face Inference API (gratuito com rate limits).

    Modelos gratuitos recomendados:
    - meta-llama/Llama-3.2-3B-Instruct (leve e rápido)
    - mistralai/Mistral-7B-Instruct-v0.3 (ótima qualidade)
    - microsoft/Phi-3-mini-4k-instruct (muito eficiente)
    - Qwen/Qwen2.5-7B-Instruct (multilíngue)
    - google/gemma-2-2b-it (compacto)

    Configuração:
    1. Crie conta em huggingface.co
    2. Gere token em: huggingface.co/settings/tokens
    3. export HF_TOKEN=seu_token_aqui
    """

    def __init__(
        self,
        model_name: str = None,
        api_key: str = None,
        config: Optional[GenerationConfig] = None
    ):
        model = model_name or os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
        super().__init__(model, config)
        self.api_key = api_key or os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        self.base_url = "https://api-inference.huggingface.co/models"
        self.timeout = int(os.getenv("HF_TIMEOUT", "60"))

    @property
    def provider_type(self) -> LLMProvider:
        return LLMProvider.HUGGINGFACE

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="HF_TOKEN não configurado. Obtenha em huggingface.co/settings/tokens"
            )

        try:
            import requests
        except ImportError:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="pip install requests"
            )

        cfg = config or self.config
        start_time = time.time()

        try:
            response = requests.post(
                f"{self.base_url}/{self.model_name}",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "inputs": prompt,
                    "parameters": {
                        "temperature": cfg.temperature,
                        "max_new_tokens": cfg.max_tokens,
                        "top_p": cfg.top_p,
                        "top_k": cfg.top_k,
                        "repetition_penalty": cfg.repeat_penalty,
                        "return_full_text": False
                    }
                },
                timeout=self.timeout
            )

            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "")
                else:
                    text = str(result)

                return LLMResponse(
                    text=text,
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=True
                )
            elif response.status_code == 503:
                # Modelo está carregando
                return LLMResponse(
                    text="",
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=False,
                    error_message="Modelo carregando. Aguarde ~30s e tente novamente."
                )
            else:
                return LLMResponse(
                    text="",
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )

        except Exception as e:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=str(e)
            )


class GroqProvider(BaseLLMProvider):
    """
    Provedor Groq (tier gratuito muito rápido - LPU inference).

    Modelos disponíveis no tier gratuito:
    - llama-3.1-70b-versatile (melhor qualidade)
    - llama-3.1-8b-instant (mais rápido)
    - llama3-groq-70b-8192-tool-use-preview (com tool use)
    - mixtral-8x7b-32768 (contexto longo)
    - gemma2-9b-it (Google Gemma)

    Rate limits gratuitos:
    - 30 requests/minuto
    - 14,400 requests/dia

    Configuração:
    1. Crie conta em console.groq.com
    2. Gere API key
    3. export GROQ_API_KEY=seu_token_aqui
    """

    def __init__(
        self,
        model_name: str = None,
        api_key: str = None,
        config: Optional[GenerationConfig] = None
    ):
        model = model_name or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        super().__init__(model, config)
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.timeout = int(os.getenv("GROQ_TIMEOUT", "30"))

    @property
    def provider_type(self) -> LLMProvider:
        return LLMProvider.GROQ

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="GROQ_API_KEY não configurado. Obtenha em console.groq.com"
            )

        try:
            import requests
        except ImportError:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="pip install requests"
            )

        cfg = config or self.config
        start_time = time.time()

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": cfg.temperature,
                    "max_tokens": cfg.max_tokens,
                    "top_p": cfg.top_p
                },
                timeout=self.timeout
            )

            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                text = result["choices"][0]["message"]["content"]
                tokens = result.get("usage", {}).get("total_tokens", 0)

                return LLMResponse(
                    text=text,
                    provider=self.provider_type,
                    model=self.model_name,
                    tokens_used=tokens,
                    latency_ms=latency,
                    success=True
                )
            else:
                return LLMResponse(
                    text="",
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )

        except Exception as e:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=str(e)
            )


class TogetherProvider(BaseLLMProvider):
    """
    Provedor Together.ai (tier gratuito com créditos iniciais).

    Modelos recomendados:
    - meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo
    - mistralai/Mixtral-8x7B-Instruct-v0.1
    - Qwen/Qwen2.5-72B-Instruct-Turbo
    - google/gemma-2-27b-it

    Configuração:
    1. Crie conta em together.ai
    2. Gere API key
    3. export TOGETHER_API_KEY=seu_token_aqui
    """

    def __init__(
        self,
        model_name: str = None,
        api_key: str = None,
        config: Optional[GenerationConfig] = None
    ):
        model = model_name or os.getenv("TOGETHER_MODEL", "meta-llama/Llama-3.2-3B-Instruct-Turbo")
        super().__init__(model, config)
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.timeout = int(os.getenv("TOGETHER_TIMEOUT", "60"))

    @property
    def provider_type(self) -> LLMProvider:
        return LLMProvider.TOGETHER

    def is_available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> LLMResponse:
        if not self.api_key:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="TOGETHER_API_KEY não configurado. Obtenha em together.ai"
            )

        try:
            import requests
        except ImportError:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message="pip install requests"
            )

        cfg = config or self.config
        start_time = time.time()

        try:
            response = requests.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": cfg.temperature,
                    "max_tokens": cfg.max_tokens,
                    "top_p": cfg.top_p,
                    "repetition_penalty": cfg.repeat_penalty
                },
                timeout=self.timeout
            )

            latency = (time.time() - start_time) * 1000

            if response.status_code == 200:
                result = response.json()
                text = result["choices"][0]["message"]["content"]
                tokens = result.get("usage", {}).get("total_tokens", 0)

                return LLMResponse(
                    text=text,
                    provider=self.provider_type,
                    model=self.model_name,
                    tokens_used=tokens,
                    latency_ms=latency,
                    success=True
                )
            else:
                return LLMResponse(
                    text="",
                    provider=self.provider_type,
                    model=self.model_name,
                    latency_ms=latency,
                    success=False,
                    error_message=f"HTTP {response.status_code}: {response.text[:200]}"
                )

        except Exception as e:
            return LLMResponse(
                text="",
                provider=self.provider_type,
                model=self.model_name,
                success=False,
                error_message=str(e)
            )


class UnifiedLLMProvider:
    """
    Provedor unificado que gerencia múltiplos backends de LLM.

    Características:
    - Fallback automático entre provedores
    - Seleção inteligente baseada em disponibilidade
    - Retry com backoff exponencial
    - Métricas de uso

    Uso:
        provider = UnifiedLLMProvider()
        response = provider.generate("Explique o Model X")
    """

    # Ordem de preferência dos provedores
    DEFAULT_PRIORITY = [
        LLMProvider.GROQ,      # Mais rápido (LPU)
        LLMProvider.OLLAMA,    # Local, sem rate limits
        LLMProvider.HUGGINGFACE,
        LLMProvider.TOGETHER
    ]

    def __init__(
        self,
        providers: Optional[Dict[LLMProvider, BaseLLMProvider]] = None,
        priority: Optional[List[LLMProvider]] = None,
        config: Optional[GenerationConfig] = None
    ):
        self.config = config or GenerationConfig()
        self.priority = priority or self.DEFAULT_PRIORITY

        # Inicializa provedores
        if providers:
            self.providers = providers
        else:
            self.providers = {
                LLMProvider.OLLAMA: OllamaProvider(config=self.config),
                LLMProvider.HUGGINGFACE: HuggingFaceProvider(config=self.config),
                LLMProvider.GROQ: GroqProvider(config=self.config),
                LLMProvider.TOGETHER: TogetherProvider(config=self.config)
            }

        # Métricas
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "provider_usage": {p.value: 0 for p in LLMProvider},
            "total_tokens": 0,
            "total_latency_ms": 0
        }

    def get_available_providers(self) -> List[LLMProvider]:
        """Retorna lista de provedores disponíveis em ordem de prioridade."""
        available = []
        for provider_type in self.priority:
            if provider_type in self.providers:
                provider = self.providers[provider_type]
                if provider.is_available():
                    available.append(provider_type)
        return available

    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        preferred_provider: Optional[LLMProvider] = None,
        max_retries: int = 3
    ) -> LLMResponse:
        """
        Gera texto usando o melhor provedor disponível.

        Args:
            prompt: Texto de entrada para o LLM
            config: Configuração de geração (opcional)
            preferred_provider: Provedor preferido (opcional)
            max_retries: Número máximo de tentativas

        Returns:
            LLMResponse com o texto gerado ou erro
        """
        self.metrics["total_requests"] += 1
        cfg = config or self.config

        # Define ordem de tentativa
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try = [preferred_provider] + [
                p for p in self.priority if p != preferred_provider
            ]
        else:
            providers_to_try = self.priority.copy()

        last_error = None

        for provider_type in providers_to_try:
            if provider_type not in self.providers:
                continue

            provider = self.providers[provider_type]

            if not provider.is_available():
                logger.info(f"Provider {provider_type.value} não disponível, pulando...")
                continue

            # Tenta com retry
            for attempt in range(max_retries):
                logger.info(f"Tentando {provider_type.value} (tentativa {attempt + 1}/{max_retries})")

                response = provider.generate(prompt, cfg)

                if response.success:
                    self.metrics["successful_requests"] += 1
                    self.metrics["provider_usage"][provider_type.value] += 1
                    self.metrics["total_tokens"] += response.tokens_used
                    self.metrics["total_latency_ms"] += response.latency_ms
                    return response

                last_error = response.error_message
                logger.warning(f"Falha no {provider_type.value}: {last_error}")

                # Backoff exponencial antes de retry
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Aguardando {wait_time}s antes de retry...")
                    time.sleep(wait_time)

        # Todos os provedores falharam
        self.metrics["failed_requests"] += 1

        return LLMResponse(
            text="Não foi possível gerar resposta. Todos os provedores falharam.",
            provider=LLMProvider.OLLAMA,  # fallback
            model="none",
            success=False,
            error_message=f"Todos os provedores falharam. Último erro: {last_error}"
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de uso."""
        metrics = self.metrics.copy()
        if metrics["successful_requests"] > 0:
            metrics["avg_latency_ms"] = metrics["total_latency_ms"] / metrics["successful_requests"]
            metrics["avg_tokens"] = metrics["total_tokens"] / metrics["successful_requests"]
        else:
            metrics["avg_latency_ms"] = 0
            metrics["avg_tokens"] = 0
        return metrics

    def get_status(self) -> Dict[str, Any]:
        """Retorna status de todos os provedores."""
        return {
            "available_providers": [p.value for p in self.get_available_providers()],
            "all_providers": {
                provider_type.value: {
                    "available": provider.is_available(),
                    "model": provider.model_name
                }
                for provider_type, provider in self.providers.items()
            },
            "metrics": self.get_metrics()
        }


# Instância global para uso simplificado
_default_provider: Optional[UnifiedLLMProvider] = None


def get_default_provider() -> UnifiedLLMProvider:
    """Retorna a instância padrão do provedor unificado."""
    global _default_provider
    if _default_provider is None:
        _default_provider = UnifiedLLMProvider()
    return _default_provider


def generate_text(
    prompt: str,
    config: Optional[GenerationConfig] = None,
    preferred_provider: Optional[LLMProvider] = None
) -> LLMResponse:
    """
    Função de conveniência para gerar texto.

    Args:
        prompt: Texto de entrada
        config: Configuração de geração
        preferred_provider: Provedor preferido

    Returns:
        LLMResponse com o texto gerado
    """
    return get_default_provider().generate(prompt, config, preferred_provider)
