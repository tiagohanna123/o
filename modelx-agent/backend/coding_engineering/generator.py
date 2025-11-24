from typing import Dict, Any
from .prompts import build_main_prompt


def call_llm(prompt: str) -> str:
    """
    Placeholder de chamada a LLM.
    TODO: integrar com provider real (OpenAI, etc.).
    """
    return "TODO: implementar chamada ao LLM"


def generate_answer(message: str,
                    energy_vector: Dict[str, float],
                    sigma_S_X: Dict[str, float],
                    state) -> Dict[str, Any]:
    prompt = build_main_prompt(message, state, energy_vector, sigma_S_X)
    raw_answer = call_llm(prompt)

    return {
        "answer_text": raw_answer,
        "energy_vector": energy_vector,
        "sigma": sigma_S_X["sigma"],
        "S": sigma_S_X["S"],
        "X": sigma_S_X["X"]
    }
