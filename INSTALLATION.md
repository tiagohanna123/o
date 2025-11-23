# Installation and Usage - Model X Framework v2.0

## 🚀 **Quick Installation**

### **Prerequisites:**
- Python 3.7+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### **1. Installation via pip:**
```bash
# Install required dependencies
pip install numpy scipy matplotlib plotly pandas

# Optional: for advanced visualizations
pip install plotly-express kaleido

# For development
pip install jupyter notebook
```

### **2. Verify installation:**
```python
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

print("Model X v2.0 - Dependencies successfully installed!")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Plotly: {go.__version__}")
```

---

## 📁 **File Structure**

```
v2_repo/
├── README.md                    # Main documentation
├── o_v2.py                     # Main Python scripts
├── o_v2.html                   # Interactive visualizations
├── scientific_paper_professional.html  # Scientific paper
├── decadimensional_model.md     # Decadimensional submodel
├── philosophical_paper_academic.md    # Philosophical analysis
├── CHANGELOG.md                # Change history
├── LICENSE                     # MIT License
└── INSTALLATION.md            # This file
```

---

## 🎯 **Basic Usage**

### **1. Run Python Simulations:**
```python
# Import module
from o_v2 import ModelXv2

# Create model instance
model = ModelXv2()

# Qubit simulation
import numpy as np
time_points = np.linspace(0, 5, 100)
qubit_data = model.simulate_qubit_decoherence(time_points)

# Biological simulation
bio_data = model.simulate_biological_system(
    time_points, 
    metabolic_rate=1.0, 
    nutrients=0.8
)

# Validate model
validation = model.validate_model(qubit_data)
print(validation)
```

### **2. Run Interactive Visualizations:**

#### **Option A: Open HTML directly**
```bash
# Navigate to directory
cd v2_repo

# Open in browser
open o_v2.html  # Mac
start o_v2.html  # Windows
xdg-open o_v2.html  # Linux
```

#### **Option B: Serve with Python**
```bash
# Start local web server
python -m http.server 8000

# Access in browser
# http://localhost:8000/o_v2.html
```

#### **Option C: Jupyter Notebook**
```python
# Create interactive notebook
import plotly.graph_objects as go
from o_v2 import ModelXv2, ModelXVisualizer

model = ModelXv2()
visualizer = ModelXVisualizer()

# Create visualization
fig = visualizer.plot_energy_modulation(energy_data)
fig.show()
```

---

## 🎮 **Interactive Features**

### **1. Fundamentals Demonstration:**
- **Sliders**: Adjust entropy, syntropy, and energy
- **Visualization**: See real-time impact
- **Interpretation**: Dynamic explanatory text

### **2. Energy Modulation:**
- **Controls**: Reference energy, α and β coefficients
- **Graphs**: Modulation functions f(ℰ) and g(ℰ)
- **Zones**: Automatic regime identification

### **3. Decadimensional Submodel:**
- **Transitions**: Simulate dimensional jumps
- **Symbology**: Numerical symbol decoding
- **Validation**: Verify allowed transitions

### **4. Practical Simulations:**
- **Quantum System**: Decoherence and coherence
- **Biological System**: Cellular metabolism
- **Economic System**: Markets and volatility
- **Network System**: Topology and traffic

---

## 📊 **Data Analysis**

### **1. Export Data:**
```python
# Export simulation to JSON
model.export_simulation_data(qubit_data, 'qubit_results.json')

# Export validation
import json
with open('validation_results.json', 'w') as f:
    json.dump(validation, f, indent=2)
```

### **2. Statistical Analysis:**
```python
# Import analysis libraries
import pandas as pd
from scipy import stats

# Load data
with open('qubit_results.json', 'r') as f:
    data = json.load(f)

# Create DataFrame
df = pd.DataFrame(data)

# Descriptive analysis
print(df.describe())

# Normality tests
shapiro_stat, shapiro_p = stats.shapiro(df['X_scalar'])
print(f"Shapiro-Wilk: p = {shapiro_p}")

# Correlations
correlation = df['X_scalar'].corr(df['temporal_dilation'])
print(f"Correlation: r = {correlation}")
```

---

## 🔧 **Advanced Settings**

### **1. Model Parameters:**
```python
# Modify model constants
model.constants['alpha'] = 0.5  # Entropic modulation
model.constants['beta'] = 0.8   # Syntropic modulation
model.constants['gamma'] = 1.5  # Modulation exponent

# Adjust reference energy
model.constants['epsilon_0'] = 2.0
```

### **2. Visualization Settings:**
```python
# Customize graphs
fig.update_layout(
    title="My Custom Simulation",
    template="plotly_dark",
    font=dict(family="Arial", size=14),
    showlegend=True
)

# Save as interactive HTML
fig.write_html("my_simulation.html")

# Save as static image
fig.write_image("my_simulation.png", width=1200, height=800)
```

---

## 🐛 **Troubleshooting**

### **Problem: Import error**
```python
# Solution: Install missing dependencies
pip install numpy scipy matplotlib plotly
```

### **Problem: Graphs don't appear**
```python
# Solution: Check matplotlib backend
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import matplotlib.pyplot as plt
```

### **Problem: Plotly doesn't render**
```python
# Solution: Use offline mode
import plotly.io as pio
pio.renderers.default = "browser"
```

### **Problem: Slow performance**
```python
# Solution: Reduce simulation resolution
# Reduce number of time points
time_points = np.linspace(0, 5, 50)  # instead of 100

# Use numba for acceleration
from numba import jit

@jit(nopython=True)
def fast_calculation(data):
    # accelerated code
    return result
```

---

## 📚 **Additional Resources**

### **1. Complete Documentation:**
- `README.md` - Overview and theory
- `scientific_paper_professional.html` - Academic paper
- `decadimensional_model.md` - Dimensional submodel
- `philosophical_paper_academic.md` - Philosophical analysis

### **2. Code Examples:**
```python
# Complete usage example
from o_v2 import ModelXv2, ModelXVisualizer

# Initialize
model = ModelXv2()
visualizer = ModelXVisualizer()

# Configure simulation
time = np.linspace(0, 10, 200)
energy = 1 + 0.3 * np.sin(time)

# Execute
qubit_data = model.simulate_qubit_decoherence(time, energy)
bio_data = model.simulate_biological_system(time, 1.2, 0.9)

# Visualize
fig1 = model.create_interactive_plot(qubit_data, 'quantum')
fig2 = model.create_interactive_plot(bio_data, 'biological')

# Save
fig1.write_html("qubit_simulation.html")
fig2.write_html("biological_simulation.html")

# Validate
validation = model.validate_model(qubit_data)
print("Validation completed:", validation)
```

---

## 🤝 **Contributing**

### **1. Report Bugs:**
Open an issue describing:
- Operating system
- Python version
- Steps to reproduce
- Error message

### **2. Suggest Improvements:**
- New features
- Performance optimizations
- Documentation improvements
- New applications

### **3. Development:**
```bash
# Fork the repository
git clone https://github.com/tiagohanna123/o.git
cd o

# Create branch for development
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push and pull request
git push origin feature/new-feature
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **Scientific Community**: For feedback and validation
- **Contributors**: For code and documentation
- **Beta Testers**: For testing and bug reports
- **Reviewers**: For suggestions and improvements

---

**🚀 Ready to explore Model X v2.0!**

**Remember**: This framework is a powerful tool for understanding and interacting with complex systems. Use it responsibly and with scientific curiosity!
