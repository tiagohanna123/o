# Simulação para QC sem IBM Quantum
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Dados simulados realistas (baseados em backends IBM real)
np.random.seed(42)
n_qubits = 50
data = []

for q in range(n_qubits):
    # Simula T2 (0.1-0.3 ms) e fidelity (0.99-0.999)
    t1 = 100 + np.random.exponential(100)  # em µs
    t2 = t1 * np.random.uniform(0.5, 1.0)
    fid = 1 - np.random.exponential(0.001, 1)[0]
    
    X = fid - (1 - min(t2/t1, 1))
    if X > 0:
        data.append({'backend':'mock_ibmq_kyoto','qubit':q,'T2':t2,'X':X})

df = pd.DataFrame(data)

# Regressão linear
m = LinearRegression().fit(df[['X']], df['T2'])
print(f'T2 = {m.intercept_:.2f} + {m.coef_[0]:.2f} X')

# Plot
plt.scatter(df['X'], df['T2'], alpha=0.6)
plt.plot(df['X'], m.predict(df[['X']]), 'r-', linewidth=2)
plt.xlabel('X = Fidelity - Decoherence')
plt.ylabel('T2 (µs)')
plt.title('Simulação QC: T2 vs X')
plt.savefig('qc.png')
print("✅ qc.png gerado com dados simulados")