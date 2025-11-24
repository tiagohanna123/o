from typing import Dict, Any


def classify_coding_subdomain(message: str) -> Dict[str, Any]:
    msg = message.lower()
    subs = []
    if any(w in msg for w in ["bug", "erro", "traceback", "exception"]):
        subs.append("debugging")
    if any(w in msg for w in ["refatore", "refatorar", "organizar código", "melhorar código"]):
        subs.append("refactoring")
    if any(w in msg for w in ["escreva uma função", "implemente", "crie um código"]):
        subs.append("code_generation")
    if any(w in msg for w in ["testes", "tests", "pytest", "unittest"]):
        subs.append("testing")
    if not subs:
        subs.append("generic")

    return {
        "domain": "coding_engineering",
        "subdomains": subs,
        "confidence": 0.9
    }
