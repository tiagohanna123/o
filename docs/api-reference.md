# API Reference - Model X Framework v3.0

Complete API documentation for the Model X Framework.

---

## Table of Contents

- [EnergyModulatedModel](#energymodulatedmodel)
- [EntropySyntropyCalculator](#entropysyntropyalculator)
- [EnergyModulationEngine](#energymodulationengine)
- [SimulationEngine](#simulationengine)
- [ModelXVisualizer](#modelxvisualizer)
- [ValidationUtils](#validationutils)

---

## EnergyModulatedModel

Main class for entropy-syntropy-energy system modeling.

### Constructor

```python
EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=1.0)
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|--------|-----------|
| entropy | float | 0.5 | Entropy level [0, ∞) → clamped ≥ 0 |
| syntropy | float | 0.5 | Syntropy level [0, ∞) → clamped ≥ 0 |
| energy | float | 1.0 | System energy [0.1, ∞) |

**Example:**
```python
from model_x import EnergyModulatedModel

model = EnergyModulatedModel(entropy=0.3, syntropy=0.7, energy=2.0)
```

### Methods

#### compute_temporal_dilation()

Calculates temporal dilation: `τ = ℰ × (1 + (S - E))`

**Returns:** `float` - Temporal dilation factor

#### compute_modulation(alpha=0.3, beta=0.7, gamma=1.5)

Calculates energy modulation functions.

**Returns:** `tuple(float, float)` - (f_E, g_S)

#### simulate(steps=100, dt=0.01)

Simulates temporal evolution.

**Returns:** `list[dict]` - List of states {step, time, dilation}

---

## EntropySyntropyCalculator

Shannon entropy and syntropy calculator.

### Methods

#### calculate_shannon_entropy(data, bins=10)

**Returns:** `float` - Normalized entropy [0, 1]

#### calculate_syntropy(data, method="complement")

**Returns:** `float` - Syntropy [0, 1]

---

## EnergyModulationEngine

Energy modulation engine.

### Methods

#### modulate_energy(entropy, syntropy, energy, modulation_type="adaptive")

**Types:** "adaptive", "conservative", "basic"

**Returns:** `tuple(float, float, tuple)` - (f_E×ℰ, g_S×ℰ, params)

---

## SimulationEngine

Temporal simulation engine.

### Constructor

```python
SimulationEngine(dt=0.01, max_steps=10000)
```

### Methods

#### run_simulation(initial_state, simulation_type="deterministic")

**Returns:** `list[dict]` - History {step, time, state, dilation}

#### get_statistics()

**Returns:** `dict` - {total_steps, mean_dilation, std_dilation}

---

## ModelXVisualizer

### Methods

- `export_simulation_data(history, filename)` - Export JSON
- `ascii_plot(data, title, width, height)` - ASCII plot
- `print_simulation_summary(history)` - Formatted summary
- `generate_report(domains_data, output_file)` - Report

---

## ValidationUtils

### Static Methods

- `validate_parameters(E, S, ℰ)` - Validates parameters
- `create_default_datasets()` - Creates 4 validation datasets
- `calculate_validation_metrics(results, expected)` - Score 0-100

---

**v3.0.0 - November 2025**
