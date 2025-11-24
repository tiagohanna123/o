from typing import Dict

DIMENSIONS = [
    "syntax",
    "semantic",
    "pragmatic",
    "computational",
    "epistemic",
    "structural",
    "dynamic",
    "social",
    "creative",
    "normative"
]

DOMAIN_BASE_ENERGY: Dict[str, Dict[str, float]] = {
    "coding_engineering": {
        "syntax": 0.8,
        "semantic": 0.6,
        "pragmatic": 0.7,
        "computational": 0.9,
        "epistemic": 0.5,
        "structural": 0.8,
        "dynamic": 0.5,
        "social": 0.3,
        "creative": 0.4,
        "normative": 0.4
    }
}


def compute_energy_vector(domain_info: dict) -> Dict[str, float]:
    domain = domain_info["domain"]
    conf = domain_info.get("confidence", 1.0)
    base = DOMAIN_BASE_ENERGY[domain].copy()
    for k in base:
        base[k] *= conf
    return base
