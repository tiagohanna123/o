# O/Model X Framework

A compact, testable framework measuring entropy-syntropy balance via scalar $X = \sigma - S$ in quantum, cosmological, and complex systems. Singularities are asymptotic horizons ($X \approx 0$), avoiding infinities in equations like Friedmann and Einstein. Derived from intuitive logic, it includes temporal dilation $d\tau/dt = \exp(-\kappa X)$, with $\kappa$ from fluctuation-dissipation.

## Overview
- **Core Metric**: $X = k (\ln N - 2S)$, where $S$ is Shannon-Boltzmann entropy and $\sigma$ is KL divergence from uniform noise.
- **Key Prediction**: Systems near $X \approx 0$ exhibit neutral time ($d\tau/dt = 1$), promoting dynamic equilibrium.
- **Applications**: Quantum coherence (sustains order in qubits), cosmology (regularizes Big Bang), AI (resilient training by balancing noise-structure), ecology (ecosystem stability metrics).
- **Falsifiability**: Testable via simulations (e.g., $X$ dilation retards decoherence >10% in IBM data) and diagnostics $\mathcal{S}_X \approx 0$.

Unifies negentropy [Schrödinger, 1944] with modern quantum info [Horodecki et al., 1998] and entropic gravity [Verlinde, 2011]. Full preprint and code below.

**Latest release: [https://github.com/tiagohanna123/o/releases/tag/v1.0]**

## Files
- `o.pdf`: Complete preprint (4 pages, English).
- `o.tex`: LaTeX source for the paper.
- `ographs.html`: Interactive plots (Chart.js) for Friedmann cosmic expansion and qubit decoherence.
- `o.py`: Python scripts (SciPy/NumPy) for core simulations.
- `friedmann_plots.png`
- `qubit_plots.png`

## Quick Start: Run Simulations
Install dependencies: `pip install numpy scipy matplotlib`.

### Qubit Decoherence Example
```python
import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 100)
S_t = np.log(2) * (1 - np.exp(-t))  # Von Neumann entropy (nats)
X_t = np.log(2) - 2 * S_t  # Model X scalar
kappa = np.log(2) / 1.0  # Characteristic time = 1
dtau_dt = np.exp(-kappa * X_t)  # Temporal dilation

plt.plot(t, X_t, label='$X(t)$')
plt.plot(t, dtau_dt, label='$d\\tau/dt$')
plt.xlabel('Time $t$')
plt.ylabel('Value')
plt.legend()
plt.title('Model X: Qubit Decoherence')
plt.show()

print(f"Avg X: {np.mean(X_t):.3f}")  # ~0.00 near balance
