# Model X Framework v3.1

**Hyperdimensional Framework for Universal Complexity Analysis**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Validation Score](https://img.shields.io/badge/validation-93.0%2F100-green.svg)](./VALIDATION_REPORT.md)

> **📋 What's New in v3.1.0**: Branch consolidation, astrophysical validations (GW150914, CMB, Quantum Computing), and IBM Quantum experiments! See the [CHANGELOG](./CHANGELOG.md) for complete details.

---

## Overview

The **Model X Framework** is a mathematical metatheory that models complex systems through fundamental relationships between:

- **Entropy (E)**: Measure of disorder/randomness (normalized Shannon)
- **Syntropy (S)**: Measure of organization/structure (complement of entropy)
- **Energy (ℰ)**: System modulating variable

### Fundamental Equation

```
Φ(E, S, ℰ) = E × f(ℰ) + S × g(ℰ) = C (conservation constant)
```

### Validation Results

| Domain | Score | Status |
|---------|-------|--------|
| Finance | 100.0/100 | ✓ Validated |
| Biology | 82.8/100 | ✓ Validated |
| Physics | 91.1/100 | ✓ Validated |
| Networks | 98.2/100 | ✓ Validated |
| **Average** | **93.0/100** | **✓ Excellence** |

---

## Installation

### Via pip (recommended)
```bash
pip install -e .
```

### Dependencies
```bash
pip install numpy scipy matplotlib
```

### For development
```bash
pip install -e ".[dev]"
```

---

## Quick Start

### Basic Example
```python
from model_x import EnergyModulatedModel

# Create model with parameters
model = EnergyModulatedModel(
    entropy=0.4,      # Disorder level
    syntropy=0.6,     # Organization level
    energy=1.5        # System energy
)

# Calculate temporal dilation
dilation = model.compute_temporal_dilation()
print(f"Temporal dilation: {dilation:.4f}")

# Calculate energy modulation
f_E, g_S = model.compute_modulation()
print(f"Entropic modulation: {f_E:.4f}")
print(f"Syntropic modulation: {g_S:.4f}")

# Simulate temporal evolution
trajectory = model.simulate(steps=100, dt=0.01)
```

### Advanced Analysis
```python
from model_x import (
    EntropySyntropyCalculator,
    SimulationEngine,
    ValidationUtils
)

# Calculate entropy from real data
calculator = EntropySyntropyCalculator()
data = [1.2, 3.4, 2.1, 4.5, 3.2, 2.8, 3.9, 4.1]

entropy = calculator.calculate_shannon_entropy(data)
syntropy = calculator.calculate_syntropy(data)

print(f"Entropy: {entropy:.4f}")
print(f"Syntropy: {syntropy:.4f}")

# Run simulation
engine = SimulationEngine(dt=0.01, max_steps=1000)
initial_state = {
    'entropy': entropy,
    'syntropy': syntropy,
    'energy': 1.0
}

history = engine.run_simulation(initial_state, 'deterministic')
stats = engine.get_statistics()

print(f"Simulated steps: {stats['total_steps']}")
print(f"Average dilation: {stats['mean_dilation']:.4f}")
```

---

## Architecture

```
model-x-framework/
├── src/model_x/
│   ├── __init__.py                  # Main API
│   ├── entropy_syntropy.py          # Entropy/syntropy calculations
│   ├── energy_modulation.py         # Energy modulation engine
│   ├── simulation_engine.py         # Temporal simulation
│   ├── visualization.py             # Visualization and export
│   ├── utils.py                     # Validation utilities
│   └── patterned_datasets.py        # Patterned datasets
├── tests/                           # Test suite (95 tests)
├── docs/                            # Complete documentation
├── examples/                        # Usage examples
└── data/                            # Validation datasets
```

---

## Main Components

### EntropySyntropyCalculator
Calculates normalized Shannon entropy and syntropy.

```python
calculator = EntropySyntropyCalculator()
entropy = calculator.calculate_shannon_entropy(data)    # [0, 1]
syntropy = calculator.calculate_syntropy(data)          # [0, 1]
```

### EnergyModulationEngine
Modulation engine with three modes: adaptive, conservative, and basic.

```python
modulator = EnergyModulationEngine()
result = modulator.modulate_energy(entropy, syntropy, energy, 'adaptive')
```

### SimulationEngine
Deterministic temporal simulation with state tracking.

```python
engine = SimulationEngine(dt=0.01, max_steps=1000)
history = engine.run_simulation(state, 'deterministic')
stats = engine.get_statistics()
```

### ValidationUtils
Utilities for validation and dataset creation.

```python
utils = ValidationUtils()
datasets = utils.create_default_datasets()
metrics = utils.calculate_validation_metrics(results, expected)
```

---

## Mathematical Foundations

### Normalized Shannon Entropy
```
H(X) = -Σ p(x) × log₂(p(x)) / log₂(N)
```
Where `N` is the number of discretization bins.

### Temporal Dilation
```
τ = τ₀ × (1 + (S - E) / ℰ)
```
Where `τ₀` is the system's proper time.

### Energy Modulation
```
f(ℰ) = 1 + α × (E / ℰ)
g(ℰ) = 1 + β × (S / ℰ)^γ
```
With default parameters: α=0.3, β=0.7, γ=1.5

### Conservation Law
```
E(+) + E(-) + S(+) + S(-) + N = C
```

---

## Tests

```bash
# Run all tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=src/model_x

# Specific tests
python -m pytest tests/test_simulation_engine.py -v
```

**Current coverage**: 95 tests, all passing.

---

## Documentation

| Document | Description |
|-----------|-----------|
| [MATHEMATICAL_FOUNDATIONS.md](./docs/MATHEMATICAL_FOUNDATIONS.md) | Complete mathematical foundations |
| [API Reference](./docs/api-reference.md) | API reference |
| [Getting Started](./docs/getting-started.md) | Quick start guide |
| [CHANGELOG](./CHANGELOG.md) | Version history |
| [Validation Report](./VALIDATION_REPORT.md) | Validation report |

---

## Application Domains

The framework has been validated across multiple domains:

1. **Finance**: Time series analysis of volatility
2. **Biology**: Heart rhythm modeling (ECG)
3. **Physics**: Oscillatory systems with harmonics
4. **Networks**: Data traffic analysis
5. **Thermodynamics**: Evolution of energy systems
6. **Quantum Computing**: Qubit states (see `quantum/`)
7. **Cosmology**: Universal expansion models

### Additional Experiments

#### Astrophysical Validations (notebooks/)
- **GW150914**: Gravitational wave validation (first direct detection 2015)
  - Script: `notebooks/gw_validation.py`
  - Maximum SNR (H1 detector): 7.4
  - Optimal κ: 0.0
  
- **CMB (Cosmic Microwave Background)**: Cosmic background radiation validation
  - Script: `notebooks/cmb_validation.py`
  - Data: `data/planck_tt.txt` (Planck data)
  
- **Quantum Computing**: Quantum circuit validation
  - Script: `notebooks/qc_validation.py`

#### IBM Quantum Experiments (quantum/)
- Experimental validation using IBM Quantum Experience
- Main script: `quantum/ibm_quantum_runner.py`
- Configuration: `quantum/quantum_config.py`
- Documentation: `quantum/README_QUANTUM.md`
- Results saved in: `quantum/results/`

```bash
# To run quantum experiments
cd quantum
pip install -r requirements_quantum.txt
python quantum_config.py  # Configure IBM Quantum credentials
python ibm_quantum_runner.py
```

---

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

```bash
# Fork and clone
git clone https://github.com/your-username/o.git

# Create branch
git checkout -b feature/new-feature

# Install development dependencies
pip install -e ".[dev]"

# Run tests before committing
python -m pytest tests/ -v
```

---

## Citation

If you use this framework in academic research:

```bibtex
@software{model_x_framework,
  author = {Hanna, Tiago},
  title = {Model X Framework: Hyperdimensional Theory of Universal Complexity},
  version = {3.1.0},
  year = {2025},
  url = {https://github.com/tiagohanna123/o}
}
```

---

## License

MIT License - see [LICENSE](./LICENSE) for details.

---

## Contact

**Author**: Tiago Hanna
**Email**: hanna@mkbl.com.br / tiagohv94@gmail.com
**GitHub**: [@tiagohanna123](https://github.com/tiagohanna123)

---

**Version**: 3.1.0
**Last Updated**: November 2025
**Status**: Production/Stable - Validated at 93.0/100
