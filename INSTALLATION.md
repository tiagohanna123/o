# Instalação e Uso - Modelo X Framework v2.0

## 🚀 **Instalação Rápida**

### **Pré-requisitos:**
- Python 3.7+
- pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### **1. Instalação via pip:**
```bash
# Instalar dependências necessárias
pip install numpy scipy matplotlib plotly pandas

# Opcional: para visualizações avançadas
pip install plotly-express kaleido

# Para desenvolvimento
pip install jupyter notebook
```

### **2. Verificação da instalação:**
```python
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

print("Modelo X v2.0 - Dependências instaladas com sucesso!")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Plotly: {go.__version__}")
```

---

## 📁 **Estrutura de Arquivos**

```
v2_repo/
├── README.md                    # Documentação principal
├── o_v2.py                     # Scripts Python principais
├── o_v2.html                   # Visualizações interativas
├── scientific_paper_professional.html  # Paper científico
├── decadimensional_model.md     # Submodelo decadimensional
├── philosophical_paper_academic.md    # Análise filosófica
├── CHANGELOG.md                # Histórico de mudanças
├── LICENSE                     # Licença MIT
└── INSTALLATION.md            # Este arquivo
```

---

## 🎯 **Uso Básico**

### **1. Executar Simulações Python:**
```python
# Importar o módulo
from o_v2 import ModelXv2

# Criar instância do modelo
model = ModelXv2()

# Simulação de qubit
import numpy as np
time_points = np.linspace(0, 5, 100)
qubit_data = model.simulate_qubit_decoherence(time_points)

# Simulação biológica
bio_data = model.simulate_biological_system(
    time_points, 
    metabolic_rate=1.0, 
    nutrients=0.8
)

# Validar modelo
validation = model.validate_model(qubit_data)
print(validation)
```

### **2. Executar Visualizações Interativas:**

#### **Opção A: Abrir HTML diretamente**
```bash
# Navegar até o diretório
cd v2_repo

# Abrir no navegador
open o_v2.html  # Mac
start o_v2.html  # Windows
xdg-open o_v2.html  # Linux
```

#### **Opção B: Servir com Python**
```bash
# Iniciar servidor web local
python -m http.server 8000

# Acessar no navegador
# http://localhost:8000/o_v2.html
```

#### **Opção C: Jupyter Notebook**
```python
# Criar notebook interativo
import plotly.graph_objects as go
from o_v2 import ModelXv2, ModelXVisualizer

model = ModelXv2()
visualizer = ModelXVisualizer()

# Criar visualização
fig = visualizer.plot_energy_modulation(energy_data)
fig.show()
```

---

## 🎮 **Funcionalidades Interativas**

### **1. Demonstração de Fundamentos:**
- **Sliders**: Ajustar entropia, syntropia e energia
- **Visualização**: Ver impacto em tempo real
- **Interpretação**: Texto explicativo dinâmico

### **2. Modulação Energética:**
- **Controles**: Energia de referência, coeficientes α e β
- **Gráficos**: Funções de modulação f(ℰ) e g(ℰ)
- **Zonas**: Identificação automática de regimes

### **3. Submodelo Decadimensional:**
- **Transições**: Simular saltos dimensionais
- **Simbologia**: Decodificação de símbolos numéricos
- **Validação**: Verificar transições permitidas

### **4. Simulações Práticas:**
- **Sistema Quântico**: Decoerência e coerência
- **Sistema Biológico**: Metabolismo celular
- **Sistema Econômico**: Mercados e volatilidade
- **Sistema de Rede**: Topologia e tráfego

---

## 📊 **Análise de Dados**

### **1. Exportar Dados:**
```python
# Exportar simulação para JSON
model.export_simulation_data(qubit_data, 'qubit_results.json')

# Exportar validação
import json
with open('validation_results.json', 'w') as f:
    json.dump(validation, f, indent=2)
```

### **2. Análise Estatística:**
```python
# Importar bibliotecas de análise
import pandas as pd
from scipy import stats

# Carregar dados
with open('qubit_results.json', 'r') as f:
    data = json.load(f)

# Criar DataFrame
df = pd.DataFrame(data)

# Análise descritiva
print(df.describe())

# Testes de normalidade
shapiro_stat, shapiro_p = stats.shapiro(df['X_scalar'])
print(f"Shapiro-Wilk: p = {shapiro_p}")

# Correlações
correlation = df['X_scalar'].corr(df['temporal_dilation'])
print(f"Correlação: r = {correlation}")
```

---

## 🔧 **Configurações Avançadas**

### **1. Parâmetros do Modelo:**
```python
# Modificar constantes do modelo
model.constants['alpha'] = 0.5  # Modulação entrópica
model.constants['beta'] = 0.8   # Modulação sintrópica
model.constants['gamma'] = 1.5  # Expoente de modulação

# Ajustar energia de referência
model.constants['epsilon_0'] = 2.0
```

### **2. Configurações de Visualização:**
```python
# Personalizar gráficos
fig.update_layout(
    title="Minha Simulação Personalizada",
    template="plotly_dark",
    font=dict(family="Arial", size=14),
    showlegend=True
)

# Salvar como HTML interativo
fig.write_html("minha_simulacao.html")

# Salvar como imagem estática
fig.write_image("minha_simulacao.png", width=1200, height=800)
```

---

## 🐛 **Solução de Problemas**

### **Problema: Erro de importação**
```python
# Solução: Instalar dependências faltantes
pip install numpy scipy matplotlib plotly
```

### **Problema: Gráficos não aparecem**
```python
# Solução: Verificar backend do matplotlib
import matplotlib
matplotlib.use('TkAgg')  # ou 'Qt5Agg'
import matplotlib.pyplot as plt
```

### **Problema: Plotly não renderiza**
```python
# Solução: Usar modo offline
import plotly.io as pio
pio.renderers.default = "browser"
```

### **Problema: Performance lenta**
```python
# Solução: Reduzir resolução da simulação
# Reduzir número de pontos de tempo
time_points = np.linspace(0, 5, 50)  # ao invés de 100

# Usar numba para aceleração
from numba import jit

@jit(nopython=True)
def fast_calculation(data):
    # código acelerado
    return result
```

---

## 📚 **Recursos Adicionais**

### **1. Documentação Completa:**
- `README.md` - Visão geral e teoria
- `scientific_paper_professional.html` - Paper acadêmico
- `decadimensional_model.md` - Submodelo dimensional
- `philosophical_paper_academic.md` - Análise filosófica

### **2. Exemplos de Código:**
```python
# Exemplo completo de uso
from o_v2 import ModelXv2, ModelXVisualizer

# Inicializar
model = ModelXv2()
visualizer = ModelXVisualizer()

# Configurar simulação
time = np.linspace(0, 10, 200)
energy = 1 + 0.3 * np.sin(time)

# Executar
qubit_data = model.simulate_qubit_decoherence(time, energy)
bio_data = model.simulate_biological_system(time, 1.2, 0.9)

# Visualizar
fig1 = model.create_interactive_plot(qubit_data, 'quantum')
fig2 = model.create_interactive_plot(bio_data, 'biological')

# Salvar
fig1.write_html("qubit_simulation.html")
fig2.write_html("biological_simulation.html")

# Validar
validation = model.validate_model(qubit_data)
print("Validação concluída:", validation)
```

---

## 🤝 **Contribuindo**

### **1. Reportar Bugs:**
Abra uma issue descrevendo:
- Sistema operacional
- Versão do Python
- Passos para reproduzir
- Mensagem de erro

### **2. Sugerir Melhorias:**
- Novas funcionalidades
- Otimizações de performance
- Melhorias na documentação
- Novas aplicações

### **3. Desenvolvimento:**
```bash
# Fork o repositório
git clone https://github.com/tiagohanna123/o.git
cd o

# Criar branch para desenvolvimento
git checkout -b feature/nova-funcionalidade

# Fazer alterações e commit
git add .
git commit -m "Adiciona nova funcionalidade"

# Push e pull request
git push origin feature/nova-funcionalidade
```

---

## 📄 **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 **Agradecimentos**

- **Comunidade Científica**: Pelo feedback e validação
- **Contribuidores**: Pelo código e documentação
- **Beta Testers**: Pelo teste e reporte de bugs
- **Revisores**: Pelas sugestões e melhorias

---

**🚀 Pronto para explorar o Modelo X v2.0!**

**Lembre-se**: Este framework é uma ferramenta poderosa para compreender e interagir com sistemas complexos. Use com responsabilidade e curiosidade científica!