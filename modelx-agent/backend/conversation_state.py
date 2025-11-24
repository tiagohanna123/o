from typing import List, Optional, Any
from dataclasses import dataclass, field
import time


@dataclass
class Message:
    role: str  # "user" ou "assistant"
    content: str
    timestamp: float


@dataclass
class RhythmStats:
    avg_latency: float = 0.0
    last_latency: float = 0.0
    avg_length: float = 0.0
    last_length: float = 0.0
    variability_latency: float = 0.0
    variability_length: float = 0.0
    estimated_state: str = "neutro"  # "apressado", "explorando", "frustrado", etc.


@dataclass
class ConversationState:
    id: str
    root_question: str
    root_question_vector: Any  # pode ser embedding
    messages: List[Message] = field(default_factory=list)
    last_answer_summary: Optional[str] = None
    last_answer_vector: Optional[Any] = None
    coherence_history: List[dict] = field(default_factory=list)
    rhythm: RhythmStats = field(default_factory=RhythmStats)


def update_rhythm_stats(state: ConversationState, new_message: str, timestamp: float) -> RhythmStats:
    length = len(new_message)
    if state.messages:
        last_ts = state.messages[-1].timestamp
        latency = timestamp - last_ts
    else:
        latency = 0.0

    r = state.rhythm
    alpha = 0.3

    if len(state.messages) > 0:
        r.avg_latency = alpha * latency + (1 - alpha) * r.avg_latency
        r.avg_length = alpha * length + (1 - alpha) * r.avg_length
        r.variability_latency = alpha * abs(latency - r.avg_latency) + (1 - alpha) * r.variability_latency
        r.variability_length = alpha * abs(length - r.avg_length) + (1 - alpha) * r.variability_length
    else:
        r.avg_latency = latency
        r.avg_length = length

    r.last_latency = latency
    r.last_length = length

    if latency < 5 and length < 100:
        r.estimated_state = "apressado"
    elif latency > 30 and length > 200:
        r.estimated_state = "explorando"
    else:
        r.estimated_state = "neutro"

    return r


def append_message(state: ConversationState, role: str, content: str, timestamp: Optional[float] = None):
    if timestamp is None:
        timestamp = time.time()
    state.messages.append(Message(role=role, content=content, timestamp=timestamp))
