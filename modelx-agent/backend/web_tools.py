"""
Web Tools - Ferramentas de acesso à internet para o Model X Agent.

Permite que a IA busque informações atualizadas na web:
- Busca via DuckDuckGo (gratuito, sem API key)
- Fetch de páginas web específicas
- Extração de conteúdo relevante

Uso:
    from web_tools import web_search, fetch_url, smart_search

    # Busca simples
    results = web_search("Python 3.13 novidades")

    # Busca inteligente (detecta necessidade automaticamente)
    info = smart_search("Qual a cotação do dólar hoje?")
"""

import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from urllib.parse import quote_plus, urlparse
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Resultado de uma busca web."""
    title: str
    url: str
    snippet: str
    source: str = "duckduckgo"

    def to_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source
        }


@dataclass
class WebContent:
    """Conteúdo extraído de uma página web."""
    url: str
    title: str
    content: str
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content[:2000] if self.content else "",
            "success": self.success,
            "error": self.error
        }


class WebSearchEngine:
    """
    Motor de busca web usando DuckDuckGo (gratuito, sem API).

    Características:
    - Não requer API key
    - Respeita rate limits
    - Extrai snippets relevantes
    - Cache de resultados
    """

    DUCKDUCKGO_URL = "https://html.duckduckgo.com/html/"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def __init__(self, cache_ttl: int = 300):
        """
        Args:
            cache_ttl: Tempo de vida do cache em segundos (default 5 min)
        """
        self.cache: Dict[str, tuple] = {}  # query -> (timestamp, results)
        self.cache_ttl = cache_ttl
        self.last_request_time = 0
        self.min_request_interval = 1.0  # segundos entre requisições

    def _rate_limit(self):
        """Aplica rate limiting para não sobrecarregar o serviço."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    def _get_cached(self, query: str) -> Optional[List[SearchResult]]:
        """Retorna resultado do cache se ainda válido."""
        if query in self.cache:
            timestamp, results = self.cache[query]
            if time.time() - timestamp < self.cache_ttl:
                logger.info(f"Cache hit para: {query}")
                return results
        return None

    def _set_cache(self, query: str, results: List[SearchResult]):
        """Salva resultado no cache."""
        self.cache[query] = (time.time(), results)

    def search(self, query: str, max_results: int = 5) -> List[SearchResult]:
        """
        Busca no DuckDuckGo.

        Args:
            query: Termo de busca
            max_results: Número máximo de resultados

        Returns:
            Lista de SearchResult
        """
        # Verifica cache
        cached = self._get_cached(query)
        if cached:
            return cached[:max_results]

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            logger.error("Instale: pip install requests beautifulsoup4")
            return []

        self._rate_limit()

        try:
            response = requests.post(
                self.DUCKDUCKGO_URL,
                data={"q": query},
                headers={"User-Agent": self.USER_AGENT},
                timeout=10
            )

            if response.status_code != 200:
                logger.error(f"Erro na busca: HTTP {response.status_code}")
                return []

            soup = BeautifulSoup(response.text, "html.parser")
            results = []

            # Extrai resultados da página
            for result_div in soup.select(".result"):
                title_elem = result_div.select_one(".result__title")
                snippet_elem = result_div.select_one(".result__snippet")
                link_elem = result_div.select_one(".result__url")

                if title_elem and snippet_elem:
                    title = title_elem.get_text(strip=True)
                    snippet = snippet_elem.get_text(strip=True)

                    # Extrai URL
                    url = ""
                    if link_elem:
                        url = link_elem.get("href", "")
                        if not url.startswith("http"):
                            url = "https://" + link_elem.get_text(strip=True)

                    results.append(SearchResult(
                        title=title,
                        url=url,
                        snippet=snippet
                    ))

                    if len(results) >= max_results:
                        break

            self._set_cache(query, results)
            logger.info(f"Busca '{query}': {len(results)} resultados")
            return results

        except Exception as e:
            logger.error(f"Erro na busca: {e}")
            return []

    def search_simple(self, query: str, max_results: int = 3) -> str:
        """
        Busca e retorna resultados formatados como texto.

        Args:
            query: Termo de busca
            max_results: Número máximo de resultados

        Returns:
            Texto formatado com os resultados
        """
        results = self.search(query, max_results)

        if not results:
            return f"Nenhum resultado encontrado para: {query}"

        text_parts = [f"**Resultados da busca para '{query}':**\n"]

        for i, r in enumerate(results, 1):
            text_parts.append(f"{i}. **{r.title}**")
            text_parts.append(f"   {r.snippet}")
            if r.url:
                text_parts.append(f"   Fonte: {r.url}")
            text_parts.append("")

        return "\n".join(text_parts)


class WebFetcher:
    """
    Busca e extrai conteúdo de páginas web.
    """

    USER_AGENT = "Mozilla/5.0 (compatible; ModelXBot/1.0)"

    def __init__(self, timeout: int = 15, max_content_length: int = 50000):
        self.timeout = timeout
        self.max_content_length = max_content_length

    def fetch(self, url: str) -> WebContent:
        """
        Busca conteúdo de uma URL.

        Args:
            url: URL para buscar

        Returns:
            WebContent com o conteúdo extraído
        """
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return WebContent(
                url=url, title="", content="",
                success=False,
                error="Instale: pip install requests beautifulsoup4"
            )

        try:
            response = requests.get(
                url,
                headers={"User-Agent": self.USER_AGENT},
                timeout=self.timeout,
                allow_redirects=True
            )

            if response.status_code != 200:
                return WebContent(
                    url=url, title="", content="",
                    success=False,
                    error=f"HTTP {response.status_code}"
                )

            # Limita tamanho do conteúdo
            content = response.text[:self.max_content_length]

            soup = BeautifulSoup(content, "html.parser")

            # Remove scripts e styles
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            # Extrai título
            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

            # Extrai texto principal
            text_content = soup.get_text(separator="\n", strip=True)

            # Limpa linhas em branco excessivas
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]
            clean_content = "\n".join(lines)

            return WebContent(
                url=url,
                title=title,
                content=clean_content[:self.max_content_length],
                success=True
            )

        except requests.exceptions.Timeout:
            return WebContent(
                url=url, title="", content="",
                success=False, error="Timeout"
            )
        except Exception as e:
            return WebContent(
                url=url, title="", content="",
                success=False, error=str(e)
            )


class SmartWebSearch:
    """
    Busca web inteligente que detecta automaticamente quando usar a internet.

    Detecta perguntas que precisam de informações atualizadas:
    - Cotações, preços, valores atuais
    - Notícias e eventos recentes
    - Documentação técnica atualizada
    - Informações que mudam com frequência
    """

    # Padrões que indicam necessidade de busca web
    NEEDS_WEB_PATTERNS = [
        # Atualidade
        r"\b(hoje|agora|atual|atualmente|recente|últim[oa]s?|nov[oa]s?)\b",
        r"\b(today|now|current|currently|recent|latest|new)\b",

        # Cotações e preços
        r"\b(cotação|preço|valor|quanto custa|quanto está)\b",
        r"\b(price|cost|value|how much)\b",

        # Notícias
        r"\b(notícia|acontec|evento|lançamento|anúncio)\b",
        r"\b(news|happened|event|release|announcement)\b",

        # Versões e atualizações
        r"\b(versão|version|update|release|v\d+)\b",

        # Documentação
        r"\b(documentação|docs|api|referência)\b",
        r"\b(documentation|reference|guide)\b",

        # Tempo e clima
        r"\b(tempo|clima|previsão|temperatura)\b",
        r"\b(weather|forecast|temperature)\b",

        # Perguntas diretas sobre fatos
        r"\b(quem é|o que é|quando foi|onde fica)\b",
        r"\b(who is|what is|when was|where is)\b",
    ]

    def __init__(self):
        self.search_engine = WebSearchEngine()
        self.fetcher = WebFetcher()
        self._patterns = [re.compile(p, re.IGNORECASE) for p in self.NEEDS_WEB_PATTERNS]

    def needs_web_search(self, query: str) -> bool:
        """
        Detecta se a query precisa de busca na web.

        Args:
            query: Pergunta do usuário

        Returns:
            True se provavelmente precisa de informações da web
        """
        for pattern in self._patterns:
            if pattern.search(query):
                return True
        return False

    def extract_search_terms(self, query: str) -> str:
        """
        Extrai termos de busca relevantes da query.

        Remove palavras comuns e mantém termos importantes.
        """
        # Remove palavras de pergunta comuns
        stop_words = {
            "o", "a", "os", "as", "um", "uma", "de", "da", "do", "em", "na", "no",
            "que", "qual", "como", "quando", "onde", "por", "para", "com",
            "the", "a", "an", "is", "are", "was", "were", "what", "how", "when", "where",
            "me", "diga", "fale", "explique", "tell", "explain", "show"
        }

        words = query.lower().split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]

        return " ".join(filtered) if filtered else query

    def search(
        self,
        query: str,
        force_search: bool = False,
        max_results: int = 3,
        fetch_content: bool = False
    ) -> Dict[str, Any]:
        """
        Busca inteligente na web.

        Args:
            query: Pergunta do usuário
            force_search: Força busca mesmo se não detectar necessidade
            max_results: Número máximo de resultados
            fetch_content: Se True, busca conteúdo completo das páginas

        Returns:
            Dict com resultados e metadados
        """
        needs_search = force_search or self.needs_web_search(query)

        if not needs_search:
            return {
                "searched": False,
                "reason": "Query não parece precisar de informações da web",
                "results": [],
                "content": ""
            }

        # Extrai termos de busca
        search_terms = self.extract_search_terms(query)
        logger.info(f"Buscando na web: '{search_terms}'")

        # Realiza busca
        results = self.search_engine.search(search_terms, max_results)

        # Formata resultados
        formatted_results = [r.to_dict() for r in results]

        # Opcionalmente busca conteúdo completo
        content_parts = []
        if fetch_content and results:
            for r in results[:2]:  # Limita a 2 páginas
                if r.url:
                    web_content = self.fetcher.fetch(r.url)
                    if web_content.success:
                        content_parts.append(f"**{web_content.title}**\n{web_content.content[:1500]}")

        # Monta contexto para o LLM
        context = self._build_context(query, results, content_parts)

        return {
            "searched": True,
            "query": query,
            "search_terms": search_terms,
            "results": formatted_results,
            "content": context,
            "sources": [r.url for r in results if r.url]
        }

    def _build_context(
        self,
        original_query: str,
        results: List[SearchResult],
        content_parts: List[str]
    ) -> str:
        """Constrói contexto formatado para o LLM."""
        parts = [
            "## Informações da Web\n",
            f"Busca realizada para: \"{original_query}\"\n"
        ]

        if results:
            parts.append("### Resultados Encontrados:\n")
            for i, r in enumerate(results, 1):
                parts.append(f"{i}. **{r.title}**")
                parts.append(f"   {r.snippet}\n")

        if content_parts:
            parts.append("\n### Conteúdo Detalhado:\n")
            parts.extend(content_parts)

        parts.append("\n---\n*Use estas informações para responder à pergunta do usuário.*")

        return "\n".join(parts)


# ============================================================================
# FUNÇÕES DE CONVENIÊNCIA
# ============================================================================

_search_engine: Optional[WebSearchEngine] = None
_smart_search: Optional[SmartWebSearch] = None


def get_search_engine() -> WebSearchEngine:
    """Retorna instância singleton do motor de busca."""
    global _search_engine
    if _search_engine is None:
        _search_engine = WebSearchEngine()
    return _search_engine


def get_smart_search() -> SmartWebSearch:
    """Retorna instância singleton da busca inteligente."""
    global _smart_search
    if _smart_search is None:
        _smart_search = SmartWebSearch()
    return _smart_search


def web_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Busca na web e retorna resultados.

    Args:
        query: Termo de busca
        max_results: Número máximo de resultados

    Returns:
        Lista de dicts com title, url, snippet
    """
    results = get_search_engine().search(query, max_results)
    return [r.to_dict() for r in results]


def web_search_text(query: str, max_results: int = 3) -> str:
    """
    Busca na web e retorna texto formatado.

    Args:
        query: Termo de busca
        max_results: Número máximo de resultados

    Returns:
        Texto formatado com os resultados
    """
    return get_search_engine().search_simple(query, max_results)


def fetch_url(url: str) -> Dict[str, Any]:
    """
    Busca conteúdo de uma URL.

    Args:
        url: URL para buscar

    Returns:
        Dict com url, title, content, success, error
    """
    fetcher = WebFetcher()
    result = fetcher.fetch(url)
    return result.to_dict()


def smart_search(query: str, force: bool = False) -> Dict[str, Any]:
    """
    Busca inteligente - detecta automaticamente se precisa da web.

    Args:
        query: Pergunta do usuário
        force: Força busca mesmo se não detectar necessidade

    Returns:
        Dict com searched, results, content, sources
    """
    return get_smart_search().search(query, force_search=force)


def needs_web(query: str) -> bool:
    """
    Verifica se uma query precisa de busca na web.

    Args:
        query: Pergunta do usuário

    Returns:
        True se provavelmente precisa de informações atualizadas
    """
    return get_smart_search().needs_web_search(query)
