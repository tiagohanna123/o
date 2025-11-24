from typing import Dict, Any
from .domains import DOMAIN_BASE_ENERGY
from .energy_model import ENTROPIC_WEIGHTS, SYNTROPIC_WEIGHTS

LEARNING_RATE = 0.01
COHERENCE_TARGET = 0.9


def update_parameters(feedback: Dict[str, Any], domain: str = "coding_engineering"):
    score = feedback["coherence_score"]
    error = COHERENCE_TARGET - score

    if feedback.get("task_type") == "refactoring":
        if feedback["delta_complexity"] > 0:
            DOMAIN_BASE_ENERGY[domain]["structural"] += LEARNING_RATE * error
            DOMAIN_BASE_ENERGY[domain]["creative"]   -= LEARNING_RATE * error

    SYNTROPIC_WEIGHTS["structural"] += 0.5 * LEARNING_RATE * error
    ENTROPIC_WEIGHTS["structural"]  -= 0.5 * LEARNING_RATE * error

    for k in SYNTROPIC_WEIGHTS:
        SYNTROPIC_WEIGHTS[k] = max(0.0, min(1.0, SYNTROPIC_WEIGHTS[k]))
        ENTROPIC_WEIGHTS[k]  = max(0.0, min(1.0, ENTROPIC_WEIGHTS[k]))
