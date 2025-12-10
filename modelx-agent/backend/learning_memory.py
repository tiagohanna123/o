"""
Learning Memory - Sistema de aprendizado e memória para o Model X Agent.

Permite que a IA aprenda e melhore com o uso:
- Memória de longo prazo (persiste entre sessões)
- Aprendizado de preferências do usuário
- Melhoria de respostas baseada em feedback
- Contexto acumulado de conversas anteriores

Compatível com qualquer LLM via interface agnóstica.

Uso:
    from learning_memory import LearningMemory, get_memory

    memory = get_memory()

    # Salvar interação
    memory.save_interaction(question, answer, feedback_score=0.9)

    # Buscar contexto relevante
    context = memory.get_relevant_context("como otimizar SQL")

    # Obter preferências aprendidas
    prefs = memory.get_user_preferences()
"""

import json
import os
import time
import hashlib
import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime, timedelta
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

# Diretório para armazenar dados de memória
MEMORY_DIR = os.getenv("MODELX_MEMORY_DIR", ".modelx_memory")

# Número máximo de interações para manter em memória
MAX_INTERACTIONS = int(os.getenv("MAX_INTERACTIONS", "1000"))

# Número de interações similares para usar como contexto
CONTEXT_WINDOW = int(os.getenv("CONTEXT_WINDOW", "5"))

# Peso mínimo de similaridade para considerar relevante
MIN_SIMILARITY = float(os.getenv("MIN_SIMILARITY", "0.3"))


# ============================================================================
# ESTRUTURAS DE DADOS
# ============================================================================

@dataclass
class Interaction:
    """Uma interação usuário-IA."""
    id: str
    timestamp: float
    question: str
    answer: str
    feedback_score: float = 0.0  # -1 a 1 (negativo=ruim, positivo=bom)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Interaction":
        return cls(**data)


@dataclass
class UserPreference:
    """Preferência aprendida do usuário."""
    key: str
    value: Any
    confidence: float  # 0 a 1
    learned_from: int  # número de interações que geraram esta preferência
    last_updated: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserPreference":
        return cls(**data)


@dataclass
class LearnedPattern:
    """Padrão aprendido de perguntas e respostas."""
    pattern_type: str  # "question_type", "topic", "style", etc.
    pattern: str
    successful_responses: List[str]
    avg_feedback: float
    occurrence_count: int
    last_seen: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LearnedPattern":
        return cls(**data)


# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def generate_id() -> str:
    """Gera ID único para interação."""
    return hashlib.md5(f"{time.time()}{os.urandom(8)}".encode()).hexdigest()[:12]


def extract_keywords(text: str) -> List[str]:
    """Extrai palavras-chave de um texto."""
    # Remove pontuação e converte para minúsculas
    text = re.sub(r'[^\w\s]', ' ', text.lower())

    # Stop words em português e inglês
    stop_words = {
        'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'da', 'do', 'em', 'na', 'no',
        'que', 'qual', 'como', 'quando', 'onde', 'por', 'para', 'com', 'se',
        'não', 'mais', 'muito', 'também', 'só', 'já', 'ainda', 'bem',
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'as', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'under', 'again', 'further', 'then',
        'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
        'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just'
    }

    words = text.split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]

    return list(set(keywords))


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcula similaridade entre dois textos usando Jaccard.

    Método simples e agnóstico - não depende de embeddings ou LLM específico.
    """
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))

    if not keywords1 or not keywords2:
        return 0.0

    intersection = keywords1 & keywords2
    union = keywords1 | keywords2

    return len(intersection) / len(union) if union else 0.0


def detect_topic(text: str) -> List[str]:
    """Detecta tópicos/categorias de um texto."""
    topics = []

    # Padrões de tópicos comuns em engenharia de software
    topic_patterns = {
        "python": r"\b(python|pip|django|flask|pandas|numpy)\b",
        "javascript": r"\b(javascript|js|node|npm|react|vue|angular)\b",
        "database": r"\b(sql|mysql|postgres|mongodb|database|query|banco)\b",
        "api": r"\b(api|rest|graphql|endpoint|http|request)\b",
        "devops": r"\b(docker|kubernetes|ci|cd|deploy|aws|azure|cloud)\b",
        "testing": r"\b(test|unittest|pytest|jest|spec|tdd)\b",
        "security": r"\b(security|auth|jwt|oauth|password|encrypt)\b",
        "performance": r"\b(performance|otimiz|speed|cache|fast|lento)\b",
        "architecture": r"\b(architecture|design|pattern|solid|clean)\b",
        "git": r"\b(git|github|commit|branch|merge|pull)\b",
        "debug": r"\b(debug|error|bug|fix|problema|erro)\b",
        "modelx": r"\b(model\s*x|entropia|sintropia|sigma)\b",
    }

    text_lower = text.lower()
    for topic, pattern in topic_patterns.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            topics.append(topic)

    return topics if topics else ["general"]


def detect_question_type(text: str) -> str:
    """Detecta o tipo de pergunta."""
    text_lower = text.lower()

    if re.search(r"\b(como|how to|como fazer)\b", text_lower):
        return "how_to"
    elif re.search(r"\b(o que|what is|qual|define)\b", text_lower):
        return "definition"
    elif re.search(r"\b(por que|why|porque)\b", text_lower):
        return "explanation"
    elif re.search(r"\b(erro|error|bug|problema|fix)\b", text_lower):
        return "debugging"
    elif re.search(r"\b(melhor|best|recomend|suggest)\b", text_lower):
        return "recommendation"
    elif re.search(r"\b(compar|vs|versus|diferença|difference)\b", text_lower):
        return "comparison"
    elif re.search(r"\b(exemplo|example|mostr|show)\b", text_lower):
        return "example"
    else:
        return "general"


# ============================================================================
# CLASSE PRINCIPAL
# ============================================================================

class LearningMemory:
    """
    Sistema de memória e aprendizado persistente.

    Características:
    - Agnóstico de LLM (funciona com qualquer provedor)
    - Persiste dados em disco (JSON)
    - Busca por similaridade sem embeddings
    - Aprende preferências do usuário
    - Melhora com feedback
    """

    def __init__(self, memory_dir: str = MEMORY_DIR, user_id: str = "default"):
        """
        Args:
            memory_dir: Diretório para armazenar dados
            user_id: Identificador do usuário (para múltiplos usuários)
        """
        self.memory_dir = Path(memory_dir)
        self.user_id = user_id
        self.user_dir = self.memory_dir / user_id

        # Cria diretórios
        self.user_dir.mkdir(parents=True, exist_ok=True)

        # Arquivos de dados
        self.interactions_file = self.user_dir / "interactions.json"
        self.preferences_file = self.user_dir / "preferences.json"
        self.patterns_file = self.user_dir / "patterns.json"
        self.stats_file = self.user_dir / "stats.json"

        # Carrega dados
        self.interactions: List[Interaction] = self._load_interactions()
        self.preferences: Dict[str, UserPreference] = self._load_preferences()
        self.patterns: Dict[str, LearnedPattern] = self._load_patterns()
        self.stats: Dict[str, Any] = self._load_stats()

        logger.info(f"Memória inicializada: {len(self.interactions)} interações carregadas")

    # ========================================================================
    # PERSISTÊNCIA
    # ========================================================================

    def _load_json(self, filepath: Path, default: Any = None) -> Any:
        """Carrega dados de arquivo JSON."""
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar {filepath}: {e}")
        return default if default is not None else {}

    def _save_json(self, filepath: Path, data: Any):
        """Salva dados em arquivo JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Erro ao salvar {filepath}: {e}")

    def _load_interactions(self) -> List[Interaction]:
        """Carrega interações do disco."""
        data = self._load_json(self.interactions_file, [])
        return [Interaction.from_dict(d) for d in data]

    def _save_interactions(self):
        """Salva interações no disco."""
        data = [i.to_dict() for i in self.interactions[-MAX_INTERACTIONS:]]
        self._save_json(self.interactions_file, data)

    def _load_preferences(self) -> Dict[str, UserPreference]:
        """Carrega preferências do disco."""
        data = self._load_json(self.preferences_file, {})
        return {k: UserPreference.from_dict(v) for k, v in data.items()}

    def _save_preferences(self):
        """Salva preferências no disco."""
        data = {k: v.to_dict() for k, v in self.preferences.items()}
        self._save_json(self.preferences_file, data)

    def _load_patterns(self) -> Dict[str, LearnedPattern]:
        """Carrega padrões do disco."""
        data = self._load_json(self.patterns_file, {})
        return {k: LearnedPattern.from_dict(v) for k, v in data.items()}

    def _save_patterns(self):
        """Salva padrões no disco."""
        data = {k: v.to_dict() for k, v in self.patterns.items()}
        self._save_json(self.patterns_file, data)

    def _load_stats(self) -> Dict[str, Any]:
        """Carrega estatísticas do disco."""
        return self._load_json(self.stats_file, {
            "total_interactions": 0,
            "total_feedback": 0,
            "avg_feedback": 0.0,
            "topics_count": {},
            "question_types_count": {},
            "first_interaction": None,
            "last_interaction": None
        })

    def _save_stats(self):
        """Salva estatísticas no disco."""
        self._save_json(self.stats_file, self.stats)

    def save_all(self):
        """Salva todos os dados."""
        self._save_interactions()
        self._save_preferences()
        self._save_patterns()
        self._save_stats()

    # ========================================================================
    # INTERAÇÕES
    # ========================================================================

    def save_interaction(
        self,
        question: str,
        answer: str,
        feedback_score: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Salva uma interação e aprende com ela.

        Args:
            question: Pergunta do usuário
            answer: Resposta da IA
            feedback_score: Avaliação (-1 a 1)
            metadata: Dados adicionais (sigma, S, X, etc.)

        Returns:
            ID da interação
        """
        # Detecta informações
        topics = detect_topic(question)
        question_type = detect_question_type(question)

        # Cria interação
        interaction = Interaction(
            id=generate_id(),
            timestamp=time.time(),
            question=question,
            answer=answer,
            feedback_score=feedback_score,
            tags=topics + [question_type],
            metadata=metadata or {}
        )

        # Adiciona à lista
        self.interactions.append(interaction)

        # Atualiza estatísticas
        self._update_stats(interaction)

        # Aprende padrões
        self._learn_from_interaction(interaction)

        # Salva
        self._save_interactions()
        self._save_stats()

        logger.info(f"Interação salva: {interaction.id} (tópicos: {topics})")
        return interaction.id

    def update_feedback(self, interaction_id: str, feedback_score: float):
        """
        Atualiza o feedback de uma interação.

        Args:
            interaction_id: ID da interação
            feedback_score: Nova avaliação (-1 a 1)
        """
        for interaction in self.interactions:
            if interaction.id == interaction_id:
                old_score = interaction.feedback_score
                interaction.feedback_score = feedback_score

                # Atualiza estatísticas
                self.stats["total_feedback"] += 1
                total = self.stats["total_interactions"]
                if total > 0:
                    # Recalcula média considerando a mudança
                    self.stats["avg_feedback"] = (
                        (self.stats["avg_feedback"] * (total - 1) + feedback_score) / total
                    )

                # Re-aprende com novo feedback
                self._learn_from_interaction(interaction)

                self._save_interactions()
                self._save_stats()

                logger.info(f"Feedback atualizado: {interaction_id} ({old_score} -> {feedback_score})")
                return

        logger.warning(f"Interação não encontrada: {interaction_id}")

    def _update_stats(self, interaction: Interaction):
        """Atualiza estatísticas com nova interação."""
        self.stats["total_interactions"] += 1

        if interaction.feedback_score != 0:
            self.stats["total_feedback"] += 1
            n = self.stats["total_feedback"]
            old_avg = self.stats["avg_feedback"]
            self.stats["avg_feedback"] = old_avg + (interaction.feedback_score - old_avg) / n

        # Conta tópicos
        for tag in interaction.tags:
            if tag not in ["general", detect_question_type(interaction.question)]:
                self.stats["topics_count"][tag] = self.stats["topics_count"].get(tag, 0) + 1

        # Conta tipos de pergunta
        q_type = detect_question_type(interaction.question)
        self.stats["question_types_count"][q_type] = self.stats["question_types_count"].get(q_type, 0) + 1

        # Timestamps
        if self.stats["first_interaction"] is None:
            self.stats["first_interaction"] = interaction.timestamp
        self.stats["last_interaction"] = interaction.timestamp

    # ========================================================================
    # APRENDIZADO
    # ========================================================================

    def _learn_from_interaction(self, interaction: Interaction):
        """Aprende padrões de uma interação."""
        # Aprende padrão de tipo de pergunta
        q_type = detect_question_type(interaction.question)
        pattern_key = f"qtype_{q_type}"

        if pattern_key not in self.patterns:
            self.patterns[pattern_key] = LearnedPattern(
                pattern_type="question_type",
                pattern=q_type,
                successful_responses=[],
                avg_feedback=0.0,
                occurrence_count=0,
                last_seen=time.time()
            )

        pattern = self.patterns[pattern_key]
        pattern.occurrence_count += 1
        pattern.last_seen = time.time()

        # Se feedback positivo, guarda resposta como exemplo de sucesso
        if interaction.feedback_score > 0.5:
            # Limita exemplos
            if len(pattern.successful_responses) < 10:
                pattern.successful_responses.append(interaction.answer[:500])

        # Atualiza média de feedback
        n = pattern.occurrence_count
        pattern.avg_feedback = pattern.avg_feedback + (interaction.feedback_score - pattern.avg_feedback) / n

        # Aprende preferências
        self._learn_preferences(interaction)

        self._save_patterns()

    def _learn_preferences(self, interaction: Interaction):
        """Aprende preferências do usuário baseado em interações."""
        # Detecta preferência de idioma
        if re.search(r'[àáâãéêíóôõúç]', interaction.question):
            self._update_preference("language", "pt-br", interaction.feedback_score)
        elif re.search(r'\b(the|is|are|what|how)\b', interaction.question.lower()):
            self._update_preference("language", "en", interaction.feedback_score)

        # Detecta preferência de verbosidade
        answer_len = len(interaction.answer)
        if interaction.feedback_score > 0.5:
            if answer_len < 200:
                self._update_preference("verbosity", "concise", interaction.feedback_score)
            elif answer_len > 800:
                self._update_preference("verbosity", "detailed", interaction.feedback_score)
            else:
                self._update_preference("verbosity", "balanced", interaction.feedback_score)

        # Detecta preferência de código
        has_code = "```" in interaction.answer
        if has_code and interaction.feedback_score > 0.5:
            self._update_preference("likes_code_examples", True, interaction.feedback_score)

        self._save_preferences()

    def _update_preference(self, key: str, value: Any, feedback: float):
        """Atualiza uma preferência baseado em feedback."""
        if key not in self.preferences:
            self.preferences[key] = UserPreference(
                key=key,
                value=value,
                confidence=0.5,
                learned_from=0,
                last_updated=time.time()
            )

        pref = self.preferences[key]

        # Só atualiza se feedback significativo
        if abs(feedback) > 0.3:
            pref.learned_from += 1
            pref.last_updated = time.time()

            # Aumenta confiança se feedback positivo, diminui se negativo
            if feedback > 0 and pref.value == value:
                pref.confidence = min(1.0, pref.confidence + 0.1)
            elif feedback > 0 and pref.value != value:
                # Considera mudar o valor
                if pref.confidence < 0.5:
                    pref.value = value
                    pref.confidence = 0.5
                else:
                    pref.confidence -= 0.1

    # ========================================================================
    # BUSCA E CONTEXTO
    # ========================================================================

    def get_relevant_context(
        self,
        query: str,
        max_results: int = CONTEXT_WINDOW,
        min_similarity: float = MIN_SIMILARITY
    ) -> List[Dict[str, Any]]:
        """
        Busca interações anteriores relevantes para a query.

        Args:
            query: Pergunta atual
            max_results: Número máximo de resultados
            min_similarity: Similaridade mínima

        Returns:
            Lista de interações relevantes ordenadas por similaridade
        """
        if not self.interactions:
            return []

        # Calcula similaridade com cada interação
        scored = []
        for interaction in self.interactions:
            sim = calculate_similarity(query, interaction.question)

            # Boost para interações com feedback positivo
            if interaction.feedback_score > 0:
                sim *= (1 + interaction.feedback_score * 0.2)

            if sim >= min_similarity:
                scored.append((sim, interaction))

        # Ordena por similaridade
        scored.sort(key=lambda x: x[0], reverse=True)

        # Retorna top resultados
        results = []
        for sim, interaction in scored[:max_results]:
            results.append({
                "question": interaction.question,
                "answer": interaction.answer,
                "similarity": sim,
                "feedback": interaction.feedback_score,
                "topics": interaction.tags
            })

        return results

    def get_context_prompt(self, query: str) -> str:
        """
        Gera um prompt de contexto baseado em interações anteriores.

        Args:
            query: Pergunta atual

        Returns:
            Texto formatado com contexto relevante
        """
        relevant = self.get_relevant_context(query)

        if not relevant:
            return ""

        parts = ["## Contexto de Interações Anteriores\n"]
        parts.append("*Baseado em conversas anteriores relevantes:*\n")

        for i, ctx in enumerate(relevant, 1):
            parts.append(f"### Exemplo {i} (similaridade: {ctx['similarity']:.0%})")
            parts.append(f"**Pergunta:** {ctx['question'][:200]}")
            parts.append(f"**Resposta:** {ctx['answer'][:300]}...")
            if ctx['feedback'] > 0:
                parts.append(f"*(Feedback positivo: {ctx['feedback']:.1f})*")
            parts.append("")

        return "\n".join(parts)

    # ========================================================================
    # PREFERÊNCIAS
    # ========================================================================

    def get_user_preferences(self) -> Dict[str, Any]:
        """
        Retorna preferências aprendidas do usuário.

        Returns:
            Dict com preferências e suas confianças
        """
        prefs = {}
        for key, pref in self.preferences.items():
            if pref.confidence > 0.5:  # Só retorna preferências com boa confiança
                prefs[key] = {
                    "value": pref.value,
                    "confidence": pref.confidence,
                    "learned_from": pref.learned_from
                }
        return prefs

    def get_preference(self, key: str, default: Any = None) -> Any:
        """
        Obtém uma preferência específica.

        Args:
            key: Chave da preferência
            default: Valor padrão se não existir

        Returns:
            Valor da preferência ou default
        """
        if key in self.preferences and self.preferences[key].confidence > 0.5:
            return self.preferences[key].value
        return default

    def get_preferences_prompt(self) -> str:
        """
        Gera prompt com preferências do usuário para o LLM.

        Returns:
            Texto formatado com preferências
        """
        prefs = self.get_user_preferences()

        if not prefs:
            return ""

        parts = ["## Preferências do Usuário (aprendidas)\n"]

        pref_descriptions = {
            "language": "Idioma preferido",
            "verbosity": "Nível de detalhe",
            "likes_code_examples": "Gosta de exemplos de código"
        }

        for key, data in prefs.items():
            desc = pref_descriptions.get(key, key)
            parts.append(f"- **{desc}:** {data['value']} (confiança: {data['confidence']:.0%})")

        return "\n".join(parts)

    # ========================================================================
    # ESTATÍSTICAS
    # ========================================================================

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso."""
        stats = self.stats.copy()

        # Adiciona informações calculadas
        stats["total_stored"] = len(self.interactions)
        stats["preferences_learned"] = len([p for p in self.preferences.values() if p.confidence > 0.5])
        stats["patterns_learned"] = len(self.patterns)

        # Tópicos mais frequentes
        if stats["topics_count"]:
            sorted_topics = sorted(stats["topics_count"].items(), key=lambda x: x[1], reverse=True)
            stats["top_topics"] = sorted_topics[:5]

        return stats

    def get_learning_summary(self) -> str:
        """
        Gera resumo do que foi aprendido.

        Returns:
            Texto formatado com resumo de aprendizado
        """
        stats = self.get_stats()
        prefs = self.get_user_preferences()

        parts = ["## Resumo de Aprendizado\n"]

        parts.append(f"**Interações totais:** {stats['total_interactions']}")
        parts.append(f"**Feedback médio:** {stats['avg_feedback']:.2f}")
        parts.append(f"**Preferências aprendidas:** {stats['preferences_learned']}")
        parts.append(f"**Padrões identificados:** {stats['patterns_learned']}")

        if stats.get("top_topics"):
            parts.append("\n**Tópicos mais frequentes:**")
            for topic, count in stats["top_topics"]:
                parts.append(f"  - {topic}: {count} interações")

        if prefs:
            parts.append("\n**Preferências confirmadas:**")
            for key, data in prefs.items():
                parts.append(f"  - {key}: {data['value']}")

        return "\n".join(parts)


# ============================================================================
# INSTÂNCIA GLOBAL
# ============================================================================

_memory_instances: Dict[str, LearningMemory] = {}


def get_memory(user_id: str = "default") -> LearningMemory:
    """
    Retorna instância de memória para um usuário.

    Args:
        user_id: ID do usuário

    Returns:
        Instância de LearningMemory
    """
    if user_id not in _memory_instances:
        _memory_instances[user_id] = LearningMemory(user_id=user_id)
    return _memory_instances[user_id]


def save_interaction(
    question: str,
    answer: str,
    feedback_score: float = 0.0,
    user_id: str = "default",
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Função de conveniência para salvar interação.

    Args:
        question: Pergunta do usuário
        answer: Resposta da IA
        feedback_score: Avaliação (-1 a 1)
        user_id: ID do usuário
        metadata: Dados adicionais

    Returns:
        ID da interação
    """
    return get_memory(user_id).save_interaction(question, answer, feedback_score, metadata)


def get_context(query: str, user_id: str = "default") -> str:
    """
    Função de conveniência para obter contexto.

    Args:
        query: Pergunta atual
        user_id: ID do usuário

    Returns:
        Prompt de contexto formatado
    """
    return get_memory(user_id).get_context_prompt(query)
