# API Reference - Modelo X Framework v3.0

Documentação completa da API do Modelo X Framework.

---

## Sumário

- [EnergyModulatedModel](#energymodulatedmodel)
- [EntropySyntropyCalculator](#entropysyntropyalculator)
- [EnergyModulationEngine](#energymodulationengine)
- [SimulationEngine](#simulationengine)
- [ModelXVisualizer](#modelxvisualizer)
- [ValidationUtils](#validationutils)

---

## EnergyModulatedModel

Classe principal para modelagem de sistemas entropia-sintropia-energia.

### Construtor

```python
EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=1.0)
```

**Parâmetros:**
| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| entropy | float | 0.5 | Nível de entropia [0, ∞) → clamped ≥ 0 |
| syntropy | float | 0.5 | Nível de sintropia [0, ∞) → clamped ≥ 0 |
| energy | float | 1.0 | Energia do sistema [0.1, ∞) |

**Exemplo:**
```python
from model_x import EnergyModulatedModel

model = EnergyModulatedModel(entropy=0.3, syntropy=0.7, energy=2.0)
```

### Métodos

#### compute_temporal_dilation()

Calcula a dilatação temporal: `τ = ℰ × (1 + (S - E))`

**Retorno:** `float` - Fator de dilatação temporal

#### compute_modulation(alpha=0.3, beta=0.7, gamma=1.5)

Calcula funções de modulação energética.

**Retorno:** `tuple(float, float)` - (f_E, g_S)

#### simulate(steps=100, dt=0.01)

Simula evolução temporal.

**Retorno:** `list[dict]` - Lista de estados {step, time, dilation}

---

## EntropySyntropyCalculator

Calculadora de entropia de Shannon e sintropia.

### Métodos

#### calculate_shannon_entropy(data, bins=10)

**Retorno:** `float` - Entropia normalizada [0, 1]

#### calculate_syntropy(data, method="complement")

**Retorno:** `float` - Sintropia [0, 1]

---

## EnergyModulationEngine

Motor de modulação energética.

### Métodos

#### modulate_energy(entropy, syntropy, energy, modulation_type="adaptive")

**Tipos:** "adaptive", "conservative", "basic"

**Retorno:** `tuple(float, float, tuple)` - (f_E×ℰ, g_S×ℰ, params)

---

## SimulationEngine

Motor de simulação temporal.

### Construtor

```python
SimulationEngine(dt=0.01, max_steps=10000)
```

### Métodos

#### run_simulation(initial_state, simulation_type="deterministic")

**Retorno:** `list[dict]` - Histórico {step, time, state, dilation}

#### get_statistics()

**Retorno:** `dict` - {total_steps, mean_dilation, std_dilation}

---

## ModelXVisualizer

### Métodos

- `export_simulation_data(history, filename)` - Exporta JSON
- `ascii_plot(data, title, width, height)` - Gráfico ASCII
- `print_simulation_summary(history)` - Resumo formatado
- `generate_report(domains_data, output_file)` - Relatório

---

## ValidationUtils

### Métodos Estáticos

- `validate_parameters(E, S, ℰ)` - Valida parâmetros
- `create_default_datasets()` - Cria 4 datasets de validação
- `calculate_validation_metrics(results, expected)` - Score 0-100

---

**v3.0.0 - Novembro 2025**
