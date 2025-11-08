import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Model X Parameters
k = 1.0  # Boltzmann-like (nats)
kappa = np.log(2) / 1.0  # Derived from FDT, tau_char = 1

print("Model X Simulations: Friedmann Expansion and Qubit Decoherence\n")

# 1. Qubit Decoherence Simulation
def qubit_decoherence(t):
    """S(t) = ln2 * (1 - exp(-t)) for von Neumann entropy (nats)"""
    S_t = np.log(2) * (1 - np.exp(-t))
    X_t = np.log(2) - 2 * S_t  # X = ln N - 2S, N=2 for qubit
    dtau_dt = np.exp(-kappa * X_t)  # Temporal dilation
    return X_t, dtau_dt

# Generate data
t_qubit = np.linspace(0, 1, 100)
X_qubit, dtau_qubit = qubit_decoherence(t_qubit)

# Plot Qubit
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(t_qubit, X_qubit, 'g-', label='$X(t)$')
plt.axhline(y=0, color='k', linestyle='--', label='$X \\approx 0$')
plt.xlabel('Time $t$')
plt.ylabel('$X(t)$')
plt.title('Qubit: X(t) Evolution')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t_qubit, dtau_qubit, 'p-', label='$d\\tau/dt$')
plt.axhline(y=1, color='k', linestyle='--', label='Neutral Time')
plt.xlabel('Time $t$')
plt.ylabel('$d\\tau/dt$')
plt.title('Qubit: Temporal Dilation')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('qubit_plots.png')  # Save for repo
plt.show()

print(f"Qubit Sim: Avg X = {np.mean(X_qubit):.3f} (near balance)")
print(f"X at t=0 (pure): {X_qubit[0]:.3f} > 0 (syntropy)")
print(f"X at t=1 (mixed): {X_qubit[-1]:.3f} < 0 (entropy)")

# 2. Friedmann Cosmic Expansion Simulation
def friedmann(y, t, rho0=1.0, G=1.0):
    """Modified Friedmann: da/dt = a * sqrt(8*pi*G*rho/3 * (1 + X/kappa)), rho = rho0 / a^3"""
    a = y[0]
    X_t = 0.1 * np.sin(10 * t)  # Oscillatory X ~0
    H = np.sqrt((8 * np.pi * G / 3) * (rho0 / a**3) * (1 + X_t / kappa))
    da_dt = a * H
    return [da_dt]

# Initial conditions: a(0) small to avoid singularity
a0 = [0.001]
t_fried = np.linspace(0.001, 5, 100)

# Solve ODE for modified
a_mod = odeint(friedmann, a0, t_fried)

# Original (X=0)
def friedmann_orig(y, t, rho0=1.0, G=1.0):
    a = y[0]
    H = np.sqrt((8 * np.pi * G / 3) * (rho0 / a**3))
    da_dt = a * H
    return [da_dt]

a_orig = odeint(friedmann_orig, a0, t_fried)

# Hubble H(t) = da/dt / a
H_mod = np.gradient(a_mod.flatten()) / a_mod.flatten() / np.gradient(t_fried)
H_orig = np.gradient(a_orig.flatten()) / a_orig.flatten() / np.gradient(t_fried)

# Plot Friedmann
plt.figure(figsize=(10, 8))
plt.subplot(2, 1, 1)
plt.plot(t_fried, a_orig, 'r--', label='a(t) Original (Singular)')
plt.plot(t_fried, a_mod, 'b-', label='a(t) Modified with X')
plt.xlabel('Time $t$')
plt.ylabel('Scale Factor $a(t)$')
plt.title('Friedmann: Scale Factor Evolution')
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)
plt.semilogy(t_fried, H_orig, 'r--', label='H(t) Original')
plt.semilogy(t_fried, H_mod, 'b-', label='H(t) Modified')
plt.xlabel('Time $t$')
plt.ylabel('Hubble Parameter $H(t)$ (log scale)')
plt.title('Friedmann: Hubble Parameter (Smoothing ±0.1%)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('friedmann_plots.png')  # Save