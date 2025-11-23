# Modelo X Framework v3.1

**Framework Hiperdimensional para Análise de Complexidade Universal**

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Validation Score](https://img.shields.io/badge/validation-93.0%2F100-green.svg)](./VALIDATION_REPORT.md)

> **📋 Novidades na v3.1.0**: Consolidação de branches, validações astrofísicas (GW150914, CMB, Quantum Computing) e experimentos IBM Quantum! Veja o [CHANGELOG](./CHANGELOG.md) para detalhes completos.

---

## Visão Geral

O **Modelo X Framework** é uma metateoria matemática que modela sistemas complexos através das relações fundamentais entre:

- **Entropia (E)**: Medida de desordem/aleatoriedade (Shannon normalizada)
- **Sintropia (S)**: Medida de organização/estrutura (complemento da entropia)
- **Energia (ℰ)**: Variável moduladora do sistema

### Equação Fundamental

```
Φ(E, S, ℰ) = E × f(ℰ) + S × g(ℰ) = C (constante de conservação)
```

### Resultados de Validação

| Domínio | Score | Status |
|---------|-------|--------|
| Finanças | 100.0/100 | ✓ Validado |
| Biologia | 82.8/100 | ✓ Validado |
| Física | 91.1/100 | ✓ Validado |
| Redes | 98.2/100 | ✓ Validado |
| **Média** | **93.0/100** | **✓ Excelência** |

---

## Instalação

### Via pip (recomendado)
```bash
pip install -e .
```

### Dependências
```bash
pip install numpy scipy matplotlib
```

### Para desenvolvimento
```bash
pip install -e ".[dev]"
```

---

## Início Rápido

### Exemplo Básico
```python
from model_x import EnergyModulatedModel

# Criar modelo com parâmetros
model = EnergyModulatedModel(
    entropy=0.4,      # Nível de desordem
    syntropy=0.6,     # Nível de organização
    energy=1.5        # Energia do sistema
)

# Calcular dilatação temporal
dilation = model.compute_temporal_dilation()
print(f"Dilatação temporal: {dilation:.4f}")

# Calcular modulação energética
f_E, g_S = model.compute_modulation()
print(f"Modulação entrópica: {f_E:.4f}")
print(f"Modulação sintrópica: {g_S:.4f}")

# Simular evolução temporal
trajectory = model.simulate(steps=100, dt=0.01)
```

### Análise Avançada
```python
from model_x import (
    EntropySyntropyCalculator,
    SimulationEngine,
    ValidationUtils
)

# Calcular entropia de dados reais
calculator = EntropySyntropyCalculator()
data = [1.2, 3.4, 2.1, 4.5, 3.2, 2.8, 3.9, 4.1]

entropy = calculator.calculate_shannon_entropy(data)
syntropy = calculator.calculate_syntropy(data)

print(f"Entropia: {entropy:.4f}")
print(f"Sintropia: {syntropy:.4f}")

# Executar simulação
engine = SimulationEngine(dt=0.01, max_steps=1000)
initial_state = {
    'entropy': entropy,
    'syntropy': syntropy,
    'energy': 1.0
}

history = engine.run_simulation(initial_state, 'deterministic')
stats = engine.get_statistics()

print(f"Passos simulados: {stats['total_steps']}")
print(f"Dilatação média: {stats['mean_dilation']:.4f}")
```

---

## Arquitetura

```
modelo-x-framework/
├── src/model_x/
│   ├── __init__.py                  # API principal
│   ├── entropy_syntropy.py          # Cálculos de entropia/sintropia
│   ├── energy_modulation.py         # Motor de modulação energética
│   ├── simulation_engine.py         # Simulação temporal
│   ├── visualization.py             # Visualização e exportação
│   ├── utils.py                     # Utilitários de validação
│   └── patterned_datasets.py        # Datasets com padrões
├── tests/                           # Suite de testes (95 testes)
├── docs/                            # Documentação completa
├── examples/                        # Exemplos de uso
└── data/                            # Datasets de validação
```

---

## Componentes Principais

### EntropySyntropyCalculator
Calcula entropia de Shannon normalizada e sintropia.

```python
calculator = EntropySyntropyCalculator()
entropy = calculator.calculate_shannon_entropy(data)    # [0, 1]
syntropy = calculator.calculate_syntropy(data)          # [0, 1]
```

### EnergyModulationEngine
Motor de modulação com três modos: adaptativo, conservativo e básico.

```python
modulator = EnergyModulationEngine()
result = modulator.modulate_energy(entropy, syntropy, energy, 'adaptive')
```

### SimulationEngine
Simulação temporal determinística com rastreamento de estado.

```python
engine = SimulationEngine(dt=0.01, max_steps=1000)
history = engine.run_simulation(state, 'deterministic')
stats = engine.get_statistics()
```

### ValidationUtils
Utilitários para validação e criação de datasets.

```python
utils = ValidationUtils()
datasets = utils.create_default_datasets()
metrics = utils.calculate_validation_metrics(results, expected)
```

---

## Fundamentos Matemáticos

### Entropia de Shannon Normalizada
```
H(X) = -Σ p(x) × log₂(p(x)) / log₂(N)
```
Onde `N` é o número de bins de discretização.

### Dilatação Temporal
```
τ = τ₀ × (1 + (S - E) / ℰ)
```
Onde `τ₀` é o tempo próprio do sistema.

### Modulação Energética
```
f(ℰ) = 1 + α × (E / ℰ)
g(ℰ) = 1 + β × (S / ℰ)^γ
```
Com parâmetros padrão: α=0.3, β=0.7, γ=1.5

### Lei de Conservação
```
E(+) + E(-) + S(+) + S(-) + N = C
```

---

## Testes

```bash
# Executar todos os testes
python -m pytest tests/ -v

# Com cobertura
python -m pytest tests/ --cov=src/model_x

# Testes específicos
python -m pytest tests/test_simulation_engine.py -v
```

**Cobertura atual**: 95 testes, todos passando.

---

## Documentação

| Documento | Descrição |
|-----------|-----------|
| [MATHEMATICAL_FOUNDATIONS.md](./docs/MATHEMATICAL_FOUNDATIONS.md) | Fundamentos matemáticos completos |
| [API Reference](./docs/api-reference.md) | Referência da API |
| [Getting Started](./docs/getting-started.md) | Guia de início rápido |
| [CHANGELOG](./CHANGELOG.md) | Histórico de versões |
| [Validation Report](./VALIDATION_REPORT.md) | Relatório de validação |

---

## Domínios de Aplicação

O framework foi validado em múltiplos domínios:

1. **Finanças**: Análise de séries temporais de volatilidade
2. **Biologia**: Modelagem de ritmos cardíacos (ECG)
3. **Física**: Sistemas oscilatórios com harmônicos
4. **Redes**: Análise de tráfego de dados
5. **Termodinâmica**: Evolução de sistemas energéticos
6. **Computação Quântica**: Estados de qubits (ver `quantum/`)
7. **Cosmologia**: Modelos de expansão universal

### Experimentos Adicionais

#### Validações Astrofísicas (notebooks/)
- **GW150914**: Validação de ondas gravitacionais (primeira detecção direta 2015)
  - Script: `notebooks/gw_validation.py`
  - SNR máximo (detector H1): 7.4
  - κ ótimo: 0.0
  
- **CMB (Cosmic Microwave Background)**: Validação da radiação cósmica de fundo
  - Script: `notebooks/cmb_validation.py`
  - Dados: `data/planck_tt.txt` (dados do Planck)
  
- **Computação Quântica**: Validação de circuitos quânticos
  - Script: `notebooks/qc_validation.py`

#### Experimentos Quânticos IBM (quantum/)
- Validação experimental usando IBM Quantum Experience
- Script principal: `quantum/ibm_quantum_runner.py`
- Configuração: `quantum/quantum_config.py`
- Documentação: `quantum/README_QUANTUM.md`
- Resultados salvos em: `quantum/results/`

```bash
# Para executar experimentos quânticos
cd quantum
pip install -r requirements_quantum.txt
python quantum_config.py  # Configurar credenciais IBM Quantum
python ibm_quantum_runner.py
```

---

## Contribuição

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](./CONTRIBUTING.md) para diretrizes.

```bash
# Fork e clone
git clone https://github.com/seu-usuario/o.git

# Criar branch
git checkout -b feature/nova-funcionalidade

# Instalar dependências de desenvolvimento
pip install -e ".[dev]"

# Executar testes antes de commitar
python -m pytest tests/ -v
```

---

## Citação

Se usar este framework em pesquisas acadêmicas:

```bibtex
@software{modelo_x_framework,
  author = {Hanna, Tiago},
  title = {Modelo X Framework: Hyperdimensional Theory of Universal Complexity},
  version = {3.1.0},
  year = {2025},
  url = {https://github.com/tiagohanna123/o}
}
```

---

## Licença

MIT License - veja [LICENSE](./LICENSE) para detalhes.

---

## Contato

**Autor**: Tiago Hanna
**Email**: hanna@mkbl.com.br / tiagohv94@gmail.com
**GitHub**: [@tiagohanna123](https://github.com/tiagohanna123)

---

**Versão**: 3.1.0
**Última atualização**: Novembro 2025
**Status**: Produção/Estável - Validado com 93.0/100
