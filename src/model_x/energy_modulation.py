# -*- coding: utf-8 -*-
"""Funções avançadas de Modulação Energética para o Modelo X Framework"""

import numpy as np

class EnergyModulationEngine:
    """Motor de modulação energética com múltiplos regimes"""
    
    def modulate_energy(self, entropy, syntropy, energy, modulation_type="adaptive"):
        """Modula energia baseada em entropia/sintropia"""
        if modulation_type == "adaptive":
            return self._adaptive_modulation(entropy, syntropy, energy)
        elif modulation_type == "conservative":
            return self._conservative_modulation(entropy, syntropy, energy)
        else:
            return self._basic_modulation(entropy, syntropy, energy)
    
    def _adaptive_modulation(self, entropy, syntropy, energy):
        """Modulação adaptativa baseada em gradientes"""
        balance = syntropy - entropy
        alpha = 0.3 + 0.2 * np.tanh(balance)
        beta = 0.7 - 0.2 * np.tanh(balance)
        gamma = 1.5
        
        f_E = 1.0 + alpha * (entropy / max(energy, 0.1))
        g_S = 1.0 + beta * (syntropy / max(energy, 0.1)) ** gamma
        
        return f_E * energy, g_S * energy, (alpha, beta, gamma)
    
    def _conservative_modulation(self, entropy, syntropy, energy):
        """Mantém energia estável com pequenos ajustes"""
        damping_factor = 0.95
        return energy * damping_factor, energy * damping_factor, (0.5, 0.5, 1.0)
    
    def _basic_modulation(self, entropy, syntropy, energy):
        """Modulação básica padrão"""
        balance = syntropy - entropy
        factor = 1.0 + 0.1 * balance
        return energy * factor, energy * factor, (0.3, 0.7, 1.0)
