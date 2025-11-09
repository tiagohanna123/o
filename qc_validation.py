#!/usr/bin/env python3
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np, pandas as pd, os

service = QiskitRuntimeService(token=os.getenv("IBMQ_TOKEN"))
data = []
for b in service.backends(operational=True)[:5]:
    props = b.properties()
    for q in range(props.num_qubits):
        t2 = props.t2(q) or props.t1(q)
        fid = props.gate_error('sx', q) if hasattr(props, 'gate_error') else 0.001
        X = (1-fid) - (1-min(t2/props.t1(q), 1))
        data.append({"q":q, "T2":t2*1e6, "X":max(X,0)})
df = pd.DataFrame(data)

from sklearn.linear_model import LinearRegression
m = LinearRegression().fit(df[["X"]], df["T2"])
print(f"T2 = {m.intercept_:.2f} + {m.coef_[0]:.2f} X")
import matplotlib.pyplot as plt
plt.scatter(df["X"], df["T2"]); plt.savefig("qc.png")