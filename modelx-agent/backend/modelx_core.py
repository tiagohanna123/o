from typing import Dict, Any


def interpret_x_result(sigma: float, S: float) -> str:
    X = sigma - S
    txt = f"Com σ={sigma:.3f} e S={S:.3f}, temos X=σ−S={X:.3f}. "
    if X > 0:
        txt += "X > 0 indica predominância de entropia: o sistema tende a ser mais dispersivo/caótico."
    elif X < 0:
        txt += "X < 0 indica predominância de sintropia: o sistema tende a maior organização/convergência."
    else:
        txt += "X = 0 indica um balanço formal entre entropia e sintropia."
    return txt


def evaluate_system_with_model_x(system: Dict[str, Any]) -> Dict[str, Any]:
    E = system["energy_vector"]
    sigma = system["sigma"]
    S = system["S"]
    X = system["X"]
    interpretation = interpret_x_result(sigma, S)
    return {
        "sigma": sigma,
        "S": S,
        "X": X,
        "interpretation": interpretation,
        "energy_vector": E
    }
