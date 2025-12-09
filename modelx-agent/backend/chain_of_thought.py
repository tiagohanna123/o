"""
Chain of Thought com Model X - Raciocínio estruturado com auto-reflexão.

Este módulo implementa um sistema avançado de Chain-of-Thought que:
1. Usa o Model X para guiar o processo de raciocínio
2. Implementa reflexão e auto-crítica
3. Ajusta dinamicamente baseado nas métricas de entropia/sintropia
4. Permite raciocínio em múltiplas etapas com verificação

A ideia central é que o Model X (X = σ - S) funciona como um "regulador"
do processo de pensamento:
- Quando X é alto (muito caos), o sistema força mais estrutura
- Quando X é baixo (muita rigidez), o sistema incentiva exploração
- No equilíbrio, permite raciocínio natural
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import logging
import json
import re

from .llm_providers import (
    UnifiedLLMProvider,
    GenerationConfig,
    LLMProvider,
    LLMResponse,
    get_default_provider
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThoughtType(str, Enum):
    """Tipos de pensamento no chain."""
    OBSERVE = "observe"       # Observar e coletar informações
    ANALYZE = "analyze"       # Analisar dados coletados
    HYPOTHESIZE = "hypothesize"  # Formular hipóteses
    VERIFY = "verify"         # Verificar hipóteses
    REFLECT = "reflect"       # Refletir sobre o processo
    CONCLUDE = "conclude"     # Tirar conclusões
    CRITIQUE = "critique"     # Auto-crítica


@dataclass
class Thought:
    """Um pensamento individual na cadeia."""
    type: ThoughtType
    content: str
    x_state: float  # Valor de X no momento do pensamento
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "content": self.content,
            "x_state": self.x_state,
            "confidence": self.confidence,
            "metadata": self.metadata
        }


@dataclass
class ChainResult:
    """Resultado de uma cadeia de pensamento."""
    thoughts: List[Thought]
    final_answer: str
    total_x_change: float
    average_confidence: float
    reflection_summary: str
    tokens_used: int
    latency_ms: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thoughts": [t.to_dict() for t in self.thoughts],
            "final_answer": self.final_answer,
            "total_x_change": self.total_x_change,
            "average_confidence": self.average_confidence,
            "reflection_summary": self.reflection_summary,
            "tokens_used": self.tokens_used,
            "latency_ms": self.latency_ms
        }


class ModelXChainOfThought:
    """
    Sistema de Chain-of-Thought guiado pelo Model X.

    O Model X atua como um "termostato cognitivo":
    - Monitora o equilíbrio entre exploração (entropia) e estrutura (sintropia)
    - Ajusta o processo de raciocínio para manter o equilíbrio
    - Implementa auto-reflexão para melhorar a qualidade das respostas

    Uso:
        cot = ModelXChainOfThought()
        result = cot.think(
            question="Como otimizar queries SQL lentas?",
            initial_x=0.4,
            context={"domain": "database"}
        )
    """

    # Prompts para cada tipo de pensamento
    THOUGHT_PROMPTS = {
        ThoughtType.OBSERVE: """
## OBSERVAÇÃO
Observe cuidadosamente a pergunta e o contexto.
Liste os elementos-chave que você identifica:
- Conceitos mencionados
- Restrições implícitas ou explícitas
- Informações que estão faltando
- Pressupostos do usuário
""",
        ThoughtType.ANALYZE: """
## ANÁLISE
Analise os elementos observados:
- Como os conceitos se relacionam?
- Quais são as causas prováveis?
- Que padrões você identifica?
- Qual a complexidade do problema?
""",
        ThoughtType.HYPOTHESIZE: """
## HIPÓTESES
Formule hipóteses baseadas na análise:
- Hipótese principal:
- Hipóteses alternativas:
- Pressupostos necessários:
- Como validar cada hipótese?
""",
        ThoughtType.VERIFY: """
## VERIFICAÇÃO
Verifique as hipóteses:
- A hipótese principal é consistente com os dados?
- Há contra-exemplos?
- Os pressupostos são razoáveis?
- Qual a confiança em cada hipótese?
""",
        ThoughtType.REFLECT: """
## REFLEXÃO (Model X)
Reflita sobre o processo de raciocínio:
- Estado atual: X = σ - S = {x:.3f}
- O raciocínio está muito disperso (alto σ)?
- O raciocínio está muito rígido (alto S)?
- O que pode ser melhorado?
- Próximos passos recomendados:
""",
        ThoughtType.CONCLUDE: """
## CONCLUSÃO
Sintetize uma resposta final:
- Resposta principal:
- Nível de confiança:
- Ressalvas importantes:
- Recomendações práticas:
""",
        ThoughtType.CRITIQUE: """
## AUTO-CRÍTICA
Avalie criticamente sua resposta:
- Pontos fortes da resposta:
- Pontos fracos ou lacunas:
- Possíveis erros ou vieses:
- Nota de qualidade (1-10):
- O que melhoraria a resposta?
"""
    }

    # Sequência padrão de pensamentos
    DEFAULT_CHAIN = [
        ThoughtType.OBSERVE,
        ThoughtType.ANALYZE,
        ThoughtType.HYPOTHESIZE,
        ThoughtType.REFLECT,
        ThoughtType.VERIFY,
        ThoughtType.CONCLUDE,
        ThoughtType.CRITIQUE
    ]

    # Sequência curta para queries simples
    SHORT_CHAIN = [
        ThoughtType.OBSERVE,
        ThoughtType.CONCLUDE
    ]

    def __init__(
        self,
        llm_provider: Optional[UnifiedLLMProvider] = None,
        base_config: Optional[GenerationConfig] = None
    ):
        """
        Inicializa o Chain of Thought.

        Args:
            llm_provider: Provedor de LLM
            base_config: Configuração base de geração
        """
        self.llm_provider = llm_provider or get_default_provider()
        self.base_config = base_config or GenerationConfig(temperature=0.4)

    def _calculate_adjusted_x(
        self,
        base_x: float,
        thought_type: ThoughtType,
        thought_index: int
    ) -> float:
        """
        Calcula X ajustado para o contexto do pensamento.

        O X é ajustado para refletir o "estado cognitivo" ideal
        para cada tipo de pensamento:
        - OBSERVE: neutro (não modificado)
        - ANALYZE: levemente mais estruturado (-0.05)
        - HYPOTHESIZE: levemente mais exploratório (+0.05)
        - VERIFY: muito estruturado (-0.1)
        - REFLECT: neutro
        - CONCLUDE: estruturado (-0.08)
        - CRITIQUE: exploratório (+0.1)
        """
        adjustments = {
            ThoughtType.OBSERVE: 0.0,
            ThoughtType.ANALYZE: -0.05,
            ThoughtType.HYPOTHESIZE: 0.05,
            ThoughtType.VERIFY: -0.1,
            ThoughtType.REFLECT: 0.0,
            ThoughtType.CONCLUDE: -0.08,
            ThoughtType.CRITIQUE: 0.1
        }

        adjustment = adjustments.get(thought_type, 0.0)

        # Decay baseado na posição (pensamentos posteriores são mais estruturados)
        position_decay = -0.02 * thought_index

        adjusted = base_x + adjustment + position_decay
        return max(-1.0, min(1.0, adjusted))

    def _build_thought_prompt(
        self,
        thought_type: ThoughtType,
        question: str,
        previous_thoughts: List[Thought],
        x_state: float,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Constrói o prompt para um tipo específico de pensamento."""

        # Contexto anterior
        if previous_thoughts:
            history = "\n\n".join([
                f"### {t.type.value.upper()}\n{t.content}"
                for t in previous_thoughts[-3:]  # Últimos 3 pensamentos
            ])
        else:
            history = "(Início do raciocínio)"

        # Prompt específico do tipo
        type_prompt = self.THOUGHT_PROMPTS.get(thought_type, "")
        if "{x:.3f}" in type_prompt:
            type_prompt = type_prompt.format(x=x_state)

        # Contexto adicional
        context_str = ""
        if context:
            context_str = f"\n## Contexto\n{json.dumps(context, indent=2, ensure_ascii=False)}\n"

        # Estado do Model X
        if x_state > 0.3:
            x_guidance = "⚠️ X alto ({:.2f}): FOQUE em estrutura e clareza.".format(x_state)
        elif x_state < -0.3:
            x_guidance = "⚠️ X baixo ({:.2f}): EXPLORE alternativas e questione premissas.".format(x_state)
        else:
            x_guidance = "✓ X equilibrado ({:.2f}): Prossiga com abordagem balanceada.".format(x_state)

        return f"""# Chain of Thought (Model X = {x_state:.3f})

{x_guidance}
{context_str}
## Pergunta Original
"{question}"

## Raciocínio Anterior
{history}

{type_prompt}

Responda de forma estruturada e concisa:"""

    def _extract_confidence(self, thought_content: str) -> float:
        """Extrai confiança do conteúdo do pensamento."""
        # Procura padrões como "confiança: 8/10", "nota: 7", etc.
        patterns = [
            r'confian[cç]a[:\s]+(\d+(?:\.\d+)?)',
            r'nota[:\s]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)/10',
            r'(\d+(?:\.\d+)?)%'
        ]

        for pattern in patterns:
            match = re.search(pattern, thought_content.lower())
            if match:
                value = float(match.group(1))
                # Normaliza para 0-1
                if value > 1:
                    value = value / 10 if value <= 10 else value / 100
                return min(1.0, max(0.0, value))

        # Default baseado no tamanho e estrutura
        if len(thought_content) < 50:
            return 0.4
        elif "não sei" in thought_content.lower() or "incerto" in thought_content.lower():
            return 0.3
        else:
            return 0.7

    def think(
        self,
        question: str,
        initial_x: float = 0.0,
        sigma: float = 0.5,
        S: float = 0.5,
        context: Optional[Dict[str, Any]] = None,
        chain_type: str = "default",
        max_thoughts: int = 7,
        preferred_provider: Optional[LLMProvider] = None
    ) -> ChainResult:
        """
        Executa uma cadeia de pensamento completa.

        Args:
            question: Pergunta a ser respondida
            initial_x: Valor inicial de X
            sigma: Entropia inicial
            S: Sintropia inicial
            context: Contexto adicional
            chain_type: "default" ou "short"
            max_thoughts: Número máximo de pensamentos
            preferred_provider: Provedor de LLM preferido

        Returns:
            ChainResult com todos os pensamentos e resposta final
        """
        start_time = time.time()
        thoughts: List[Thought] = []
        total_tokens = 0

        # Seleciona cadeia
        if chain_type == "short":
            chain = self.SHORT_CHAIN
        else:
            chain = self.DEFAULT_CHAIN[:max_thoughts]

        current_x = initial_x
        x_history = [initial_x]

        for i, thought_type in enumerate(chain):
            # Calcula X ajustado
            adjusted_x = self._calculate_adjusted_x(current_x, thought_type, i)

            # Constrói prompt
            prompt = self._build_thought_prompt(
                thought_type=thought_type,
                question=question,
                previous_thoughts=thoughts,
                x_state=adjusted_x,
                context=context
            )

            # Configura geração baseada no tipo de pensamento
            config = GenerationConfig(
                temperature=0.3 if thought_type in [ThoughtType.VERIFY, ThoughtType.CONCLUDE] else 0.5,
                max_tokens=500 if thought_type != ThoughtType.CONCLUDE else 1000
            )

            # Gera pensamento
            response = self.llm_provider.generate(
                prompt,
                config=config,
                preferred_provider=preferred_provider
            )

            if not response.success:
                logger.warning(f"Falha em {thought_type.value}: {response.error_message}")
                continue

            total_tokens += response.tokens_used

            # Extrai confiança
            confidence = self._extract_confidence(response.text)

            # Cria pensamento
            thought = Thought(
                type=thought_type,
                content=response.text,
                x_state=adjusted_x,
                confidence=confidence,
                metadata={"tokens": response.tokens_used, "provider": response.provider.value}
            )
            thoughts.append(thought)

            # Atualiza X baseado no pensamento
            # Se o pensamento foi estruturado (alta confiança), reduz X
            # Se foi exploratório (baixa confiança), aumenta X
            x_delta = (0.5 - confidence) * 0.1
            current_x = max(-1.0, min(1.0, current_x + x_delta))
            x_history.append(current_x)

        # Extrai resposta final
        final_answer = ""
        reflection_summary = ""

        for thought in reversed(thoughts):
            if thought.type == ThoughtType.CONCLUDE:
                final_answer = thought.content
            elif thought.type == ThoughtType.REFLECT:
                reflection_summary = thought.content
            elif thought.type == ThoughtType.CRITIQUE and not reflection_summary:
                reflection_summary = thought.content

        if not final_answer and thoughts:
            final_answer = thoughts[-1].content

        # Calcula métricas
        total_x_change = x_history[-1] - x_history[0] if x_history else 0
        avg_confidence = sum(t.confidence for t in thoughts) / len(thoughts) if thoughts else 0

        latency = (time.time() - start_time) * 1000

        return ChainResult(
            thoughts=thoughts,
            final_answer=final_answer,
            total_x_change=total_x_change,
            average_confidence=avg_confidence,
            reflection_summary=reflection_summary,
            tokens_used=total_tokens,
            latency_ms=latency
        )

    def quick_think(
        self,
        question: str,
        x_state: float = 0.0,
        preferred_provider: Optional[LLMProvider] = None
    ) -> str:
        """
        Pensamento rápido para queries simples.

        Args:
            question: Pergunta
            x_state: Estado de X
            preferred_provider: Provedor preferido

        Returns:
            Resposta como string
        """
        result = self.think(
            question=question,
            initial_x=x_state,
            chain_type="short",
            max_thoughts=2,
            preferred_provider=preferred_provider
        )
        return result.final_answer


class ReflectiveReasoner:
    """
    Reasoner com reflexão iterativa baseado no Model X.

    Implementa um loop de raciocínio-reflexão-ajuste:
    1. Gera resposta inicial
    2. Reflete sobre a qualidade
    3. Se necessário, ajusta e regenera
    4. Repete até convergir ou atingir limite
    """

    def __init__(
        self,
        llm_provider: Optional[UnifiedLLMProvider] = None,
        max_iterations: int = 3,
        convergence_threshold: float = 0.8
    ):
        """
        Args:
            llm_provider: Provedor de LLM
            max_iterations: Máximo de iterações reflexivas
            convergence_threshold: Confiança mínima para parar
        """
        self.llm_provider = llm_provider or get_default_provider()
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.cot = ModelXChainOfThought(self.llm_provider)

    def _reflect_on_answer(
        self,
        question: str,
        answer: str,
        x_state: float,
        preferred_provider: Optional[LLMProvider] = None
    ) -> Dict[str, Any]:
        """Reflete sobre uma resposta e sugere melhorias."""

        prompt = f"""# Reflexão sobre Resposta (Model X)

## Estado Atual
X = {x_state:.3f}

## Pergunta Original
"{question}"

## Resposta Atual
{answer}

## Tarefa de Reflexão
Avalie criticamente a resposta acima:

1. **Completude** (0-10): A resposta cobre todos os aspectos da pergunta?
2. **Clareza** (0-10): A resposta é clara e compreensível?
3. **Precisão** (0-10): As informações estão corretas?
4. **Praticidade** (0-10): A resposta é útil e aplicável?

5. **Pontos a Melhorar**: Liste 2-3 aspectos específicos que podem ser melhorados.

6. **Nota Final** (0-10): Avaliação geral da resposta.

7. **Recomendação**: APROVAR se nota >= 8, REVISAR se nota < 8.

Responda de forma estruturada:"""

        response = self.llm_provider.generate(
            prompt,
            config=GenerationConfig(temperature=0.2, max_tokens=500),
            preferred_provider=preferred_provider
        )

        if not response.success:
            return {"approved": True, "score": 0.7, "feedback": "Reflexão indisponível"}

        text = response.text.lower()

        # Extrai nota
        score = 0.7
        patterns = [r'nota final[:\s]+(\d+)', r'(\d+)/10']
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                score = float(match.group(1)) / 10
                break

        # Determina aprovação
        approved = "aprovar" in text or score >= 0.8

        return {
            "approved": approved,
            "score": score,
            "feedback": response.text,
            "tokens": response.tokens_used
        }

    def _improve_answer(
        self,
        question: str,
        previous_answer: str,
        feedback: str,
        x_state: float,
        preferred_provider: Optional[LLMProvider] = None
    ) -> str:
        """Melhora uma resposta baseado no feedback."""

        prompt = f"""# Melhoria de Resposta (Model X)

## Estado: X = {x_state:.3f}

## Pergunta
"{question}"

## Resposta Anterior
{previous_answer}

## Feedback da Reflexão
{feedback}

## Tarefa
Gere uma VERSÃO MELHORADA da resposta, corrigindo os pontos fracos identificados.
Mantenha os pontos fortes e melhore os fracos.

Resposta Melhorada:"""

        response = self.llm_provider.generate(
            prompt,
            config=GenerationConfig(temperature=0.3, max_tokens=1500),
            preferred_provider=preferred_provider
        )

        return response.text if response.success else previous_answer

    def reason(
        self,
        question: str,
        sigma: float = 0.5,
        S: float = 0.5,
        context: Optional[Dict[str, Any]] = None,
        preferred_provider: Optional[LLMProvider] = None
    ) -> Dict[str, Any]:
        """
        Executa raciocínio reflexivo iterativo.

        Args:
            question: Pergunta a ser respondida
            sigma: Entropia
            S: Sintropia
            context: Contexto adicional
            preferred_provider: Provedor preferido

        Returns:
            Dict com resposta final, histórico de iterações e métricas
        """
        X = sigma - S
        iterations = []
        total_tokens = 0
        start_time = time.time()

        # Primeira resposta via Chain of Thought
        cot_result = self.cot.think(
            question=question,
            initial_x=X,
            sigma=sigma,
            S=S,
            context=context,
            chain_type="default",
            preferred_provider=preferred_provider
        )

        current_answer = cot_result.final_answer
        total_tokens += cot_result.tokens_used

        iterations.append({
            "iteration": 0,
            "answer": current_answer,
            "confidence": cot_result.average_confidence,
            "x_state": X
        })

        # Loop reflexivo
        for i in range(self.max_iterations):
            # Reflete
            reflection = self._reflect_on_answer(
                question, current_answer, X, preferred_provider
            )
            total_tokens += reflection.get("tokens", 0)

            if reflection["approved"] or reflection["score"] >= self.convergence_threshold:
                logger.info(f"Resposta aprovada na iteração {i+1}")
                break

            # Melhora
            improved_answer = self._improve_answer(
                question, current_answer, reflection["feedback"], X, preferred_provider
            )

            # Atualiza X baseado na melhoria
            X = X * 0.9  # Decai em direção ao equilíbrio

            current_answer = improved_answer
            iterations.append({
                "iteration": i + 1,
                "answer": current_answer,
                "confidence": reflection["score"],
                "feedback": reflection["feedback"],
                "x_state": X
            })

        latency = (time.time() - start_time) * 1000

        return {
            "final_answer": current_answer,
            "iterations": iterations,
            "total_iterations": len(iterations),
            "final_confidence": iterations[-1]["confidence"] if iterations else 0,
            "tokens_used": total_tokens,
            "latency_ms": latency,
            "converged": len(iterations) < self.max_iterations + 1
        }


# Instâncias globais
_default_cot: Optional[ModelXChainOfThought] = None
_default_reflective: Optional[ReflectiveReasoner] = None


def get_chain_of_thought() -> ModelXChainOfThought:
    """Retorna instância padrão do Chain of Thought."""
    global _default_cot
    if _default_cot is None:
        _default_cot = ModelXChainOfThought()
    return _default_cot


def get_reflective_reasoner() -> ReflectiveReasoner:
    """Retorna instância padrão do Reflective Reasoner."""
    global _default_reflective
    if _default_reflective is None:
        _default_reflective = ReflectiveReasoner()
    return _default_reflective


def think(question: str, **kwargs) -> ChainResult:
    """Função de conveniência para Chain of Thought."""
    return get_chain_of_thought().think(question, **kwargs)


def reflect_and_reason(question: str, **kwargs) -> Dict[str, Any]:
    """Função de conveniência para raciocínio reflexivo."""
    return get_reflective_reasoner().reason(question, **kwargs)
