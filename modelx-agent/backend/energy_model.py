from typing import Dict
from .conversation_state import RhythmStats
from .domains import DIMENSIONS

ENTROPIC_WEIGHTS: Dict[str, float] = {
    "syntax": 0.4,
    "semantic": 0.5,
    "pragmatic": 0.3,
    "computational": 0.2,
    "epistemic": 0.7,
    "structural": 0.1,
    "dynamic": 0.3,
    "social": 0.5,
    "creative": 0.9,
    "normative": 0.1
}

SYNTROPIC_WEIGHTS: Dict[str, float] = {
    "syntax": 0.3,
    "semantic": 0.4,
    "pragmatic": 0.5,
    "computational": 0.8,
    "epistemic": 0.4,
    "structural": 0.9,
    "dynamic": 0.6,
    "social": 0.6,
    "creative": 0.3,
    "normative": 0.9
}


def adjust_energy_with_rhythm(E: Dict[str, float], rhythm: RhythmStats) -> Dict[str, float]:
    E = E.copy()

    if rhythm.estimated_state == "apressado":
        E["pragmatic"] += 0.1
        E["normative"] += 0.1
        E["creative"]  -= 0.1
    elif rhythm.estimated_state == "explorando":
        E["creative"]  += 0.1
        E["semantic"]  += 0.1
        E["normative"] -= 0.1
    elif rhythm.estimated_state == "frustrado":
        E["structural"] += 0.15
        E["epistemic"]  += 0.15
        E["creative"]   -= 0.1

    for k in DIMENSIONS:
        if k in E:
            E[k] = max(0.0, min(1.0, E[k]))
    return E


def compute_sigma_S_from_energy(E: Dict[str, float]) -> Dict[str, float]:
    sigma = sum(E[k] * ENTROPIC_WEIGHTS[k] for k in E)
    S     = sum(E[k] * SYNTROPIC_WEIGHTS[k] for k in E)
    X     = sigma - S
    return {"sigma": sigma, "S": S, "X": X}
