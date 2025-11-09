import numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
np.random.seed(42)
n_qubits=50
data=[]
for q in range(n_qubits):
    t1=100+np.random.exponential(100)
    t2=t1*np.random.uniform(0.5,1.0)
    fid=1-np.random.exponential(0.001,1)[0]
    X=fid-(1-min(t2/t1,1))
    if X>0:
        data.append({"backend":"mock_ibmq_kyoto","qubit":q,"T2":t2,"X":X})
df=pd.DataFrame(data)
m=LinearRegression().fit(df[["X"]],df["T2"])
print(f"T2 = {m.intercept_:.2f} + {m.coef_[0]:.2f} X")
plt.scatter(df["X"],df["T2"],alpha=0.6)
plt.plot(df["X"],m.predict(df[["X"]]),"r-",linewidth=2)
plt.xlabel("X = Fidelity - Decoherence")
plt.ylabel("T2 (us)")
plt.title("QC Simulation: T2 vs X")
plt.savefig("qc.png")
print("qc.png gerado")