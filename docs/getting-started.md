# Guia de Início Rápido - Modelo X Framework v3.0

Este guia ajudará você a começar a usar o Modelo X Framework em minutos.

---

## Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes)

---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/tiagohanna123/o.git
cd o
```

### 2. Instale as dependências

```bash
pip install numpy scipy matplotlib
```

### 3. Instale o framework (modo desenvolvimento)

```bash
pip install -e .
```

---

## Primeiro Exemplo

### Passo 1: Importar o módulo

```python
from model_x import EnergyModulatedModel
```

### Passo 2: Criar um modelo

```python
# Sistema com organização moderada
model = EnergyModulatedModel(
    entropy=0.4,    # 40% desordem
    syntropy=0.6,   # 60% organização
    energy=1.0      # Energia unitária
)
```

### Passo 3: Calcular métricas

```python
# Dilatação temporal
dilation = model.compute_temporal_dilation()
print(f"Dilatação temporal: {dilation:.4f}")
# Saída: Dilatação temporal: 1.2000

# Modulação energética
f_E, g_S = model.compute_modulation()
print(f"f(E): {f_E:.4f}, g(S): {g_S:.4f}")
```

### Passo 4: Simular evolução

```python
# Simular 100 passos
trajectory = model.simulate(steps=100, dt=0.01)

# Ver alguns pontos
for point in trajectory[:5]:
    print(f"t={point['time']:.2f}: Ä={point['dilation']:.4f}")
```

---

## Análise de Dados Reais

### Calcular Entropia de Dados

```python
from model_x import EntropySyntropyCalculator
import numpy as np

# Criar calculadora
calc = EntropySyntropyCalculator()

# Seus dados
data = [1.2, 3.4, 2.1, 4.5, 3.2, 2.8, 3.9, 4.1, 2.5, 3.7]

# Calcular entropia e sintropia
entropy = calc.calculate_shannon_entropy(data)
syntropy = calc.calculate_syntropy(data)

print(f"Entropia: {entropy:.4f}")
print(f"Sintropia: {syntropy:.4f}")
print(f"Soma: {entropy + syntropy:.4f}")  # ~1.0
```

---

## Simulação Avançada

### Usando SimulationEngine

```python
from model_x import SimulationEngine

# Configurar motor de simulação
engine = SimulationEngine(
    dt=0.01,        # Intervalo de tempo
    max_steps=1000  # Máximo de passos
)

# Estado inicial
initial_state = {
    'entropy': 0.3,
    'syntropy': 0.7,
    'energy': 2.0
}

# Executar simulação
history = engine.run_simulation(initial_state, 'deterministic')

# Estatísticas
stats = engine.get_statistics()
print(f"Passos: {stats['total_steps']}")
print(f"Dilatação média: {stats['mean_dilation']:.4f}")
print(f"Desvio padrão: {stats['std_dilation']:.4f}")
```

---

## Validação

### Executar Validação Completa

```python
from model_x import ValidationUtils, EntropySyntropyCalculator, SimulationEngine

# Criar componentes
utils = ValidationUtils()
calc = EntropySyntropyCalculator()
engine = SimulationEngine(max_steps=50)

# Carregar datasets de validação
datasets = utils.create_default_datasets()

# Validar cada domínio
for name, dataset in datasets.items():
    data = dataset['data']

    # Calcular métricas
    entropy = calc.calculate_shannon_entropy(data)
    syntropy = calc.calculate_syntropy(data)

    # Simular
    state = {'entropy': entropy, 'syntropy': syntropy, 'energy': 1.0}
    history = engine.run_simulation(state, 'deterministic')

    # Métricas de validação
    results = {
        'final_state': history[-1]['state'],
        'statistics': engine.get_statistics(),
        'history': history
    }
    metrics = utils.calculate_validation_metrics(results, dataset)

    print(f"{name}: Score = {metrics['validation_score']:.1f}/100")
```

---

## Visualização

### Gráfico ASCII

```python
from model_x import ModelXVisualizer

viz = ModelXVisualizer()

# Dados de exemplo
data = [1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4]

# Criar gráfico ASCII
plot = viz.ascii_plot(data, title="Meus Dados", width=40, height=10)
print(plot)
```

### Exportar para JSON

```python
# Exportar simulação
viz.export_simulation_data(history, 'minha_simulacao.json')
```

---

## Próximos Passos

1. Leia a [Documentação Matemática](./MATHEMATICAL_FOUNDATIONS.md)
2. Explore a [Referência da API](./api-reference.md)
3. Veja os [Exemplos](../examples/)
4. Execute os [Testes](../tests/)

---

## Resolução de Problemas

### ImportError: No module named 'model_x'

```bash
# Certifique-se de estar no diretório correto
cd /caminho/para/o

# Instale em modo desenvolvimento
pip install -e .
```

### ModuleNotFoundError: numpy

```bash
pip install numpy scipy matplotlib
```

---

## Contato

Dúvidas? Entre em contato:
- GitHub: [@tiagohanna123](https://github.com/tiagohanna123)
- Email: hanna@mkbl.com.br

---

**v3.0.0 - Novembro 2025**
