from typing import Dict, Any
from ..conversation_state import ConversationState


def run_static_checks_and_tests(answer: Dict[str, Any]) -> Dict[str, Any]:
    # TODO: integrar com compilação/lint/testes reais
    return {
        "compile_ok": True,
        "lint_errors": 0,
        "tests_run": 0,
        "tests_failed": 0,
        "delta_complexity": 0.0,
        "delta_duplication": 0.0
    }


def coherence_score(feedback: Dict[str, Any]) -> float:
    score = 1.0

    if not feedback["compile_ok"]:
        score -= 0.4
    if feedback["tests_failed"] > 0:
        score -= 0.3

    score += 0.2 * (1 - min(feedback["lint_errors"] / 10, 1))
    score += 0.2 * feedback["explanation_match_score"]
    score += 0.3 * feedback["root_alignment_score"]

    score -= 0.1 * max(feedback["delta_complexity"], 0)
    score -= 0.1 * max(feedback["delta_duplication"], 0)

    return max(0.0, min(1.0, score))


def answer_root_alignment_score(state: ConversationState, answer_text: str) -> float:
    # TODO: usar LLM de self-critique que compara resposta à root_question
    return 0.8


def evaluate_coherence(message: str,
                       answer: Dict[str, Any],
                       state: ConversationState) -> Dict[str, Any]:
    static = run_static_checks_and_tests(answer)

    # TODO: explanation_match_score via LLM comparando código↔texto
    explanation_match_score = 0.8
    root_align = answer_root_alignment_score(state, answer["answer_text"])

    fb = {
        **static,
        "explanation_match_score": explanation_match_score,
        "root_alignment_score": root_align,
        "task_type": "generic"
    }
    fb["coherence_score"] = coherence_score(fb)
    return fb
