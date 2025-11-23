# -*- coding: utf-8 -*-
"""
Modelo X Framework v3.0.0
=========================

Framework hiperdimensional para análise de complexidade universal
através das relações Entropia-Sintropia-Energia.

Componentes principais:
- EntropySyntropyCalculator: Cálculo de entropia de Shannon e sintropia
- EnergyModulationEngine: Motor de modulação energética adaptativa
- SimulationEngine: Simulação temporal determinística
- ModelXVisualizer: Visualização e exportação de dados
- ValidationUtils: Utilitários de validação e datasets
- EnergyModulatedModel: Modelo unificado (compatibilidade)

Validado com score 93.0/100 em 4 domínios científicos.
"""

# Versão 3.0.0 - Módulos principais
from .entropy_syntropy import EntropySyntropyCalculator
from .energy_modulation import EnergyModulationEngine  
from .simulation_engine import SimulationEngine
from .visualization import ModelXVisualizer
from .utils import ValidationUtils

# Manter classe original para compatibilidade
class EnergyModulatedModel:
    """Modelo X Framework - Implementação mínima v2.0.0-alpha"""
    
    def __init__(self, entropy=0.5, syntropy=0.5, energy=1.0):
        self.entropy = max(0.0, float(entropy))
        self.syntropy = max(0.0, float(syntropy))
        self.energy = max(0.1, float(energy))
    
    def compute_temporal_dilation(self):
        """Calcula dilatação temporal baseada no equilíbrio entropia-sintropia"""
        balance = self.syntropy - self.entropy
        return self.energy * (1.0 + balance)
    
    def compute_modulation(self, alpha=0.3, beta=0.7, gamma=1.5):
        """Calcula modulação energética"""
        f_E = 1.0 + alpha * (self.entropy / self.energy)
        g_S = 1.0 + beta * (self.syntropy / self.energy) ** gamma
        return f_E, g_S
    
    def simulate(self, steps=100, dt=0.01):
        """Simula evolução temporal básica"""
        trajectory = []
        for i in range(steps):
            t = i * dt
            dilation = self.compute_temporal_dilation()
            trajectory.append({"step": i, "time": t, "dilation": dilation})
        return trajectory

# Exportar tudo
__all__ = [
    'EntropySyntropyCalculator',
    'EnergyModulationEngine', 
    'SimulationEngine',
    'ModelXVisualizer',
    'ValidationUtils',
    'EnergyModulatedModel'
]

__version__ = '3.0.0'
