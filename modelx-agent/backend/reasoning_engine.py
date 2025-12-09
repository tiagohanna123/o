"""
Model X Reasoning Engine - Sistema de reasoning baseado no Model X.

Este módulo implementa uma lógica de reasoning que usa o Model X (X = σ - S)
para guiar o processo de pensamento e geração de respostas.

Conceitos principais:
- σ (sigma): Entropia - mede desordem, incerteza, caos
- S: Sintropia - mede ordem, estrutura, organização
- X = σ - S: Saldo de entropia (negativo = mais estruturado)

O reasoning adapta sua estratégia baseado no estado atual do sistema:
- X alto (>0.3): Sistema caótico → estratégia de estruturação
- X baixo (<-0.3): Sistema rígido → estratégia de exploração
- X equilibrado: Estratégia balanceada

Integra com LLMs open source para geração de texto.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import logging
import json

from .llm_providers import (
    UnifiedLLMProvider,
    LLMResponse,
    GenerationConfig,
    LLMProvider,
    get_default_provider
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReasoningStrategy(str, Enum):
    """Estratégias de reasoning baseadas no estado do Model X."""
    STRUCTURING = "structuring"      # X alto: precisa estruturar
    EXPLORING = "exploring"          # X baixo: precisa flexibilizar
    BALANCED = "balanced"            # X equilibrado: abordagem balanceada
    DEEP_ANALYSIS = "deep_analysis"  # Para problemas complexos
    QUICK_RESPONSE = "quick_response"  # Para queries simples


class ReasoningPhase(str, Enum):
    """Fases do processo de reasoning."""
    ANALYSIS = "analysis"           # Analisar a pergunta
    PLANNING = "planning"           # Planejar abordagem
    EXECUTION = "execution"         # Executar raciocínio
    SYNTHESIS = "synthesis"         # Sintetizar resposta
    EVALUATION = "evaluation"       # Avaliar qualidade


@dataclass
class ThoughtStep:
    """Um passo no processo de reasoning."""
    phase: ReasoningPhase
    content: str
    confidence: float  # 0-1
    energy_state: Dict[str, float] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase.value,
            "content": self.content,
            "confidence": self.confidence,
            "energy_state": self.energy_state,
            "timestamp": self.timestamp
        }


@dataclass
class ReasoningResult:
    """Resultado do processo de reasoning."""
    answer: str
    thought_chain: List[ThoughtStep]
    strategy_used: ReasoningStrategy
    final_x_state: Dict[str, float]
    confidence: float
    provider_used: str
    latency_ms: float
    success: bool
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "answer": self.answer,
            "thought_chain": [t.to_dict() for t in self.thought_chain],
            "strategy_used": self.strategy_used.value,
            "final_x_state": self.final_x_state,
            "confidence": self.confidence,
            "provider_used": self.provider_used,
            "latency_ms": self.latency_ms,
            "success": self.success,
            "error_message": self.error_message
        }


class ModelXReasoningEngine:
    """
    Motor de reasoning que usa o Model X como framework de decisão.

    O Model X guia o processo de reasoning através de:
    1. Análise do estado atual (σ, S, X)
    2. Seleção de estratégia apropriada
    3. Chain-of-thought adaptativo
    4. Auto-avaliação e ajuste

    Exemplo:
        engine = ModelXReasoningEngine()
        result = engine.reason(
            question="Como otimizar este código?",
            sigma=0.6, S=0.3, X=0.3,
            energy_vector={...}
        )
    """

    # Thresholds para seleção de estratégia
    HIGH_ENTROPY_THRESHOLD = 0.3
    LOW_ENTROPY_THRESHOLD = -0.3

    # Prompts base para cada estratégia
    STRATEGY_PROMPTS = {
        ReasoningStrategy.STRUCTURING: """
Você está em um estado de ALTA ENTROPIA (X={x:.3f}).
Há muita incerteza e desordem. Sua abordagem deve ser:
1. PRIORIZAR clareza e estrutura
2. DIVIDIR o problema em partes menores
3. DEFINIR conceitos antes de elaborar
4. USAR listas e passos numerados
5. EVITAR divagações - seja direto
""",
        ReasoningStrategy.EXPLORING: """
Você está em um estado de ALTA SINTROPIA (X={x:.3f}).
O sistema está muito rígido. Sua abordagem deve ser:
1. EXPLORAR alternativas e perspectivas diferentes
2. QUESTIONAR premissas estabelecidas
3. CONSIDERAR soluções não-convencionais
4. MANTER abertura para mudanças
5. EVITAR respostas muito prescritivas
""",
        ReasoningStrategy.BALANCED: """
Você está em EQUILÍBRIO (X={x:.3f}).
Estado ideal para análise. Sua abordagem deve ser:
1. BALANCEAR estrutura com flexibilidade
2. ANALISAR com profundidade adequada
3. FORNECER contexto quando relevante
4. SUGERIR próximos passos práticos
5. MANTER objetividade
""",
        ReasoningStrategy.DEEP_ANALYSIS: """
Este é um problema COMPLEXO que requer análise profunda.
Sua abordagem deve ser:
1. DECOMPOR o problema em subproblemas
2. ANALISAR cada aspecto sistematicamente
3. IDENTIFICAR relações e dependências
4. CONSIDERAR edge cases e exceções
5. SINTETIZAR uma solução abrangente
""",
        ReasoningStrategy.QUICK_RESPONSE: """
Esta é uma query SIMPLES que requer resposta direta.
Sua abordagem deve ser:
1. RESPONDER diretamente à pergunta
2. SER conciso e preciso
3. EVITAR elaborações desnecessárias
4. INCLUIR código se relevante
"""
    }

    def __init__(
        self,
        llm_provider: Optional[UnifiedLLMProvider] = None,
        config: Optional[GenerationConfig] = None
    ):
        """
        Inicializa o motor de reasoning.

        Args:
            llm_provider: Provedor de LLM (usa padrão se não fornecido)
            config: Configuração de geração
        """
        self.llm_provider = llm_provider or get_default_provider()
        self.config = config or GenerationConfig(temperature=0.3)

    def select_strategy(
        self,
        x_value: float,
        question: str,
        context_complexity: float = 0.5
    ) -> ReasoningStrategy:
        """
        Seleciona a estratégia de reasoning baseada no estado do Model X.

        Args:
            x_value: Valor de X = σ - S
            question: Pergunta do usuário
            context_complexity: Complexidade estimada do contexto (0-1)

        Returns:
            Estratégia de reasoning apropriada
        """
        # Detecta queries simples
        simple_patterns = [
            "o que é", "what is",
            "defina", "define",
            "como se diz", "how to say",
            "qual o", "what's the"
        ]
        question_lower = question.lower()

        is_simple = any(p in question_lower for p in simple_patterns) and len(question) < 100

        if is_simple and context_complexity < 0.3:
            return ReasoningStrategy.QUICK_RESPONSE

        # Detecta problemas complexos
        complex_patterns = [
            "arquitetura", "architecture",
            "refatorar", "refactor",
            "otimizar", "optimize",
            "design pattern", "padrão de projeto",
            "como implementar", "how to implement"
        ]

        is_complex = any(p in question_lower for p in complex_patterns) or len(question) > 300

        if is_complex and context_complexity > 0.7:
            return ReasoningStrategy.DEEP_ANALYSIS

        # Seleção baseada no X
        if x_value > self.HIGH_ENTROPY_THRESHOLD:
            return ReasoningStrategy.STRUCTURING
        elif x_value < self.LOW_ENTROPY_THRESHOLD:
            return ReasoningStrategy.EXPLORING
        else:
            return ReasoningStrategy.BALANCED

    def _build_analysis_prompt(
        self,
        question: str,
        sigma: float,
        S: float,
        X: float,
        energy_vector: Dict[str, float]
    ) -> str:
        """Constrói prompt para fase de análise."""
        return f"""# Análise da Pergunta (Model X Reasoning)

## Estado do Sistema
- σ (entropia): {sigma:.3f}
- S (sintropia): {S:.3f}
- X (saldo): {X:.3f}

## Vetor de Energia
{json.dumps(energy_vector, indent=2)}

## Pergunta do Usuário
"{question}"

## Tarefa
Analise a pergunta e identifique:
1. Tipo de pergunta (conceitual, prática, debug, arquitetura)
2. Conceitos-chave mencionados
3. Contexto implícito necessário
4. Complexidade estimada (1-10)
5. Aspectos que precisam de esclarecimento

Responda de forma estruturada:"""

    def _build_planning_prompt(
        self,
        question: str,
        analysis: str,
        strategy: ReasoningStrategy,
        X: float
    ) -> str:
        """Constrói prompt para fase de planejamento."""
        strategy_guide = self.STRATEGY_PROMPTS[strategy].format(x=X)

        return f"""# Planejamento de Resposta (Model X Reasoning)

## Estratégia Selecionada: {strategy.value}
{strategy_guide}

## Análise Prévia
{analysis}

## Pergunta Original
"{question}"

## Tarefa
Planeje como responder a pergunta:
1. Pontos principais a cobrir
2. Ordem lógica de apresentação
3. Exemplos ou código necessários
4. Possíveis armadilhas a evitar

Plano estruturado:"""

    def _build_execution_prompt(
        self,
        question: str,
        analysis: str,
        plan: str,
        strategy: ReasoningStrategy,
        sigma: float,
        S: float,
        X: float,
        context: Optional[str] = None
    ) -> str:
        """Constrói prompt para fase de execução."""
        strategy_guide = self.STRATEGY_PROMPTS[strategy].format(x=X)

        context_section = f"\n## Contexto Adicional\n{context}\n" if context else ""

        return f"""# Model X Agent - Resposta Final

## IDENTIDADE
Você é o Model X Agent, especialista em engenharia de software.
Use o Modelo X (X = σ - S) para guiar suas respostas.

## ESTADO ATUAL
- σ (entropia/caos): {sigma:.3f}
- S (sintropia/ordem): {S:.3f}
- X (saldo): {X:.3f}

## ESTRATÉGIA
{strategy_guide}

## ANÁLISE DA PERGUNTA
{analysis}

## PLANO DE RESPOSTA
{plan}
{context_section}
## PERGUNTA DO USUÁRIO
"{question}"

## INSTRUÇÕES
1. Siga o plano estruturado
2. Use a estratégia indicada
3. Inclua código quando relevante (com markdown)
4. Seja didático mas conciso
5. Mantenha foco na pergunta original
6. Responda em português (a menos que pergunta seja em inglês)

## SUA RESPOSTA
"""

    def _evaluate_confidence(
        self,
        response: str,
        question: str,
        strategy: ReasoningStrategy
    ) -> float:
        """
        Avalia a confiança na resposta gerada.

        Heurísticas:
        - Resposta muito curta: baixa confiança
        - Resposta muito longa: pode ter divagado
        - Código presente quando esperado: aumenta confiança
        - Erro mencionado: reduz confiança
        """
        confidence = 0.7  # Base

        # Tamanho da resposta
        response_len = len(response)
        if response_len < 50:
            confidence -= 0.2
        elif response_len > 3000:
            confidence -= 0.1

        # Código quando apropriado
        code_patterns = ["código", "code", "implementar", "implement", "função", "function"]
        needs_code = any(p in question.lower() for p in code_patterns)
        has_code = "```" in response

        if needs_code and has_code:
            confidence += 0.1
        elif needs_code and not has_code:
            confidence -= 0.15

        # Erros ou incerteza
        error_patterns = ["não sei", "i don't know", "não tenho certeza", "not sure", "erro"]
        has_uncertainty = any(p in response.lower() for p in error_patterns)
        if has_uncertainty:
            confidence -= 0.1

        # Estratégia quick_response deve ser curta
        if strategy == ReasoningStrategy.QUICK_RESPONSE and response_len > 500:
            confidence -= 0.1

        return max(0.0, min(1.0, confidence))

    def reason(
        self,
        question: str,
        sigma: float,
        S: float,
        X: float,
        energy_vector: Dict[str, float],
        context: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None,
        preferred_provider: Optional[LLMProvider] = None,
        full_chain: bool = True
    ) -> ReasoningResult:
        """
        Executa o processo de reasoning completo.

        Args:
            question: Pergunta do usuário
            sigma: Valor de entropia
            S: Valor de sintropia
            X: Saldo de entropia (sigma - S)
            energy_vector: Vetor de energia 10D
            context: Contexto adicional (opcional)
            conversation_history: Histórico da conversa (opcional)
            preferred_provider: Provedor de LLM preferido
            full_chain: Se True, executa chain completo; se False, resposta direta

        Returns:
            ReasoningResult com a resposta e cadeia de pensamento
        """
        start_time = time.time()
        thought_chain: List[ThoughtStep] = []

        # 1. Seleciona estratégia
        context_complexity = 0.5
        if conversation_history:
            context_complexity = min(1.0, len(conversation_history) * 0.1 + 0.3)

        strategy = self.select_strategy(X, question, context_complexity)
        logger.info(f"Estratégia selecionada: {strategy.value} (X={X:.3f})")

        # Para respostas rápidas ou quando full_chain=False, pula análise e planejamento
        if strategy == ReasoningStrategy.QUICK_RESPONSE or not full_chain:
            # Prompt direto simplificado
            prompt = self._build_execution_prompt(
                question=question,
                analysis="Query simples - resposta direta",
                plan="Responder objetivamente",
                strategy=strategy,
                sigma=sigma, S=S, X=X,
                context=context
            )

            response = self.llm_provider.generate(
                prompt,
                config=self.config,
                preferred_provider=preferred_provider
            )

            if not response.success:
                return ReasoningResult(
                    answer=f"Erro ao gerar resposta: {response.error_message}",
                    thought_chain=[],
                    strategy_used=strategy,
                    final_x_state={"sigma": sigma, "S": S, "X": X},
                    confidence=0.0,
                    provider_used=response.provider.value,
                    latency_ms=(time.time() - start_time) * 1000,
                    success=False,
                    error_message=response.error_message
                )

            confidence = self._evaluate_confidence(response.text, question, strategy)

            return ReasoningResult(
                answer=response.text,
                thought_chain=[ThoughtStep(
                    phase=ReasoningPhase.EXECUTION,
                    content="Resposta direta gerada",
                    confidence=confidence,
                    energy_state={"sigma": sigma, "S": S, "X": X}
                )],
                strategy_used=strategy,
                final_x_state={"sigma": sigma, "S": S, "X": X},
                confidence=confidence,
                provider_used=response.provider.value,
                latency_ms=(time.time() - start_time) * 1000,
                success=True
            )

        # 2. Fase de Análise
        analysis_prompt = self._build_analysis_prompt(
            question, sigma, S, X, energy_vector
        )

        analysis_response = self.llm_provider.generate(
            analysis_prompt,
            config=GenerationConfig(temperature=0.2, max_tokens=500),
            preferred_provider=preferred_provider
        )

        if not analysis_response.success:
            logger.warning(f"Falha na análise: {analysis_response.error_message}")
            analysis = "Análise indisponível"
        else:
            analysis = analysis_response.text

        thought_chain.append(ThoughtStep(
            phase=ReasoningPhase.ANALYSIS,
            content=analysis,
            confidence=0.8 if analysis_response.success else 0.3,
            energy_state={"sigma": sigma, "S": S, "X": X}
        ))

        # 3. Fase de Planejamento
        planning_prompt = self._build_planning_prompt(
            question, analysis, strategy, X
        )

        planning_response = self.llm_provider.generate(
            planning_prompt,
            config=GenerationConfig(temperature=0.2, max_tokens=400),
            preferred_provider=preferred_provider
        )

        if not planning_response.success:
            logger.warning(f"Falha no planejamento: {planning_response.error_message}")
            plan = "Plano básico: responder diretamente"
        else:
            plan = planning_response.text

        thought_chain.append(ThoughtStep(
            phase=ReasoningPhase.PLANNING,
            content=plan,
            confidence=0.75 if planning_response.success else 0.4,
            energy_state={"sigma": sigma, "S": S, "X": X}
        ))

        # 4. Fase de Execução
        execution_prompt = self._build_execution_prompt(
            question=question,
            analysis=analysis,
            plan=plan,
            strategy=strategy,
            sigma=sigma, S=S, X=X,
            context=context
        )

        execution_response = self.llm_provider.generate(
            execution_prompt,
            config=self.config,
            preferred_provider=preferred_provider
        )

        if not execution_response.success:
            return ReasoningResult(
                answer=f"Erro ao gerar resposta: {execution_response.error_message}",
                thought_chain=thought_chain,
                strategy_used=strategy,
                final_x_state={"sigma": sigma, "S": S, "X": X},
                confidence=0.0,
                provider_used=execution_response.provider.value,
                latency_ms=(time.time() - start_time) * 1000,
                success=False,
                error_message=execution_response.error_message
            )

        answer = execution_response.text

        thought_chain.append(ThoughtStep(
            phase=ReasoningPhase.EXECUTION,
            content=f"Resposta gerada ({len(answer)} chars)",
            confidence=0.8,
            energy_state={"sigma": sigma, "S": S, "X": X}
        ))

        # 5. Fase de Avaliação
        confidence = self._evaluate_confidence(answer, question, strategy)

        thought_chain.append(ThoughtStep(
            phase=ReasoningPhase.EVALUATION,
            content=f"Confiança avaliada: {confidence:.2f}",
            confidence=confidence,
            energy_state={"sigma": sigma, "S": S, "X": X}
        ))

        total_latency = (time.time() - start_time) * 1000

        return ReasoningResult(
            answer=answer,
            thought_chain=thought_chain,
            strategy_used=strategy,
            final_x_state={"sigma": sigma, "S": S, "X": X},
            confidence=confidence,
            provider_used=execution_response.provider.value,
            latency_ms=total_latency,
            success=True
        )

    def reason_simple(
        self,
        question: str,
        sigma: float = 0.5,
        S: float = 0.5,
        preferred_provider: Optional[LLMProvider] = None
    ) -> str:
        """
        Interface simplificada para reasoning rápido.

        Args:
            question: Pergunta do usuário
            sigma: Entropia (default 0.5)
            S: Sintropia (default 0.5)
            preferred_provider: Provedor preferido

        Returns:
            Texto da resposta
        """
        X = sigma - S
        energy_vector = {
            "syntax": 0.5, "semantic": 0.5, "pragmatic": 0.5,
            "computational": 0.5, "epistemic": 0.5, "structural": 0.5,
            "dynamic": 0.5, "social": 0.5, "creative": 0.5, "normative": 0.5
        }

        result = self.reason(
            question=question,
            sigma=sigma,
            S=S,
            X=X,
            energy_vector=energy_vector,
            preferred_provider=preferred_provider,
            full_chain=False
        )

        return result.answer


# Funções de conveniência
_default_engine: Optional[ModelXReasoningEngine] = None


def get_reasoning_engine() -> ModelXReasoningEngine:
    """Retorna a instância padrão do motor de reasoning."""
    global _default_engine
    if _default_engine is None:
        _default_engine = ModelXReasoningEngine()
    return _default_engine


def reason(
    question: str,
    sigma: float,
    S: float,
    X: float,
    energy_vector: Dict[str, float],
    **kwargs
) -> ReasoningResult:
    """Função de conveniência para reasoning completo."""
    return get_reasoning_engine().reason(
        question=question,
        sigma=sigma,
        S=S,
        X=X,
        energy_vector=energy_vector,
        **kwargs
    )


def quick_reason(question: str, **kwargs) -> str:
    """Função de conveniência para reasoning rápido."""
    return get_reasoning_engine().reason_simple(question, **kwargs)
