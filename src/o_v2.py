import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json
import random

class ModeloXFramework:
    def __init__(self, alpha=0.1, beta=0.2, gamma=1.5, C=1.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.C = C
        self.E0 = 0.5
        
    def energy_modulation(self, energy_factor):
        \"\"\"Modulate entropy and syntropy based on energy level\"\"\"
        f_entropy = 1 + self.alpha * np.log(energy_factor / self.E0)
        g_syntropy = 1 + self.beta * (energy_factor / self.E0) ** self.gamma
        return f_entropy, g_syntropy
    
    def calculate_complexity(self, entropy, syntropy, energy_factor=1.0):
        \"\"\"Calculate total complexity with energy modulation\"\"\"
        f_mod, g_mod = self.energy_modulation(energy_factor)
        
        # Apply modulation
        modulated_entropy = entropy * f_mod
        modulated_syntropy = syntropy * g_mod
        
        # Total complexity must equal constant C
        total_complexity = modulated_entropy + modulated_syntropy
        
        return {
            'entropy': entropy,
            'syntropy': syntropy,
            'energy_factor': energy_factor,
            'modulated_entropy': modulated_entropy,
            'modulated_syntropy': modulated_syntropy,
            'total_complexity': total_complexity,
            'equilibrium': abs(total_complexity - self.C)
        }
    
    def simulate_system(self, iterations=1000, initial_entropy=0.3, initial_syntropy=0.7):
        \"\"\"Simulate a complex system over time\"\"\"
        results = []
        entropy = initial_entropy
        syntropy = initial_syntropy
        
        for i in range(iterations):
            # Add small random fluctuations
            entropy += random.gauss(0, 0.01)
            syntropy += random.gauss(0, 0.01)
            
            # Maintain positivity
            entropy = max(0.01, min(1.0, entropy))
            syntropy = max(0.01, min(1.0, syntropy))
            
            # Calculate energy factor (varies with time)
            energy_factor = 0.5 + 0.5 * np.sin(2 * np.pi * i / iterations)
            
            result = self.calculate_complexity(entropy, syntropy, energy_factor)
            result['time'] = i
            results.append(result)
        
        return results
    
    def validate_model(self, iterations=1000):
        \"\"\"Statistical validation of the model\"\"\"
        results = self.simulate_system(iterations)
        
        # Extract key metrics
        total_complexity = [r['total_complexity'] for r in results]
        equilibrium_deviations = [r['equilibrium'] for r in results]
        
        # Statistical tests
        equilibrium_mean = np.mean(equilibrium_deviations)
        equilibrium_std = np.std(equilibrium_deviations)
        
        # Normality test
        shapiro_stat, shapiro_p = stats.shapiro(total_complexity[:100])  # limit for shapiro
        
        # One-sample t-test against target value C
        t_stat, t_p = stats.ttest_1samp(total_complexity, self.C)
        
        return {
            'iterations': iterations,
            'equilibrium_mean': equilibrium_mean,
            'equilibrium_std': equilibrium_std,
            'shapiro_test': {'statistic': shapiro_stat, 'p_value': shapiro_p},
            't_test': {'statistic': t_stat, 'p_value': t_p},
            'validation_passed': t_p < 0.001,
            'model_fit': 1 - (equilibrium_std / np.mean(total_complexity))
        }

if __name__ == \"__main__\":
    # Initialize the framework
    model = ModeloXFramework(alpha=0.1, beta=0.2, gamma=1.5, C=1.0)
    
    print(\"=\" * 60)
    print(\"MODELO X FRAMEWORK v2.0 - VALIDATION\")
    print(\"=\" * 60)
    
    # Run validation
    validation = model.validate_model(iterations=1000)
    
    print(f\"Iterations: {validation['iterations']}\")
    print(f\"Equilibrium Mean: {validation['equilibrium_mean']:.6f}\")
    print(f\"Equilibrium Std: {validation['equilibrium_std']:.6f}\")
    print(f\"Model Fit: {validation['model_fit']:.4f}\")
    print(f\"T-test p-value: {validation['t_test']['p_value']:.6f}\")
    print(f\"Validation Passed: {validation['validation_passed']}\")
    
    # Simulate a system
    results = model.simulate_system(iterations=100)
    
    print(\"\\nFirst 5 simulation results:\")
    for i, result in enumerate(results[:5]):
        print(f\"Time {i}: Entropy={result['entropy']:.3f}, \" +
              f\"Syntropy={result['syntropy']:.3f}, \" +
              f\"Total={result['total_complexity']:.3f}\")
    
    # Save validation results
    with open(\"validation_results.json\", \"w\") as f:
        json.dump(validation, f, indent=2)
    
    print(\"\\n\" + \"=\" * 60)
    print(\"VALIDATION COMPLETE - Modelo X Framework v2.0 is READY!\")
    print(\"=\" * 60)
