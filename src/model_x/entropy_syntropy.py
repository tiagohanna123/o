# -*- coding: utf-8 -*-
"""Cálculos fundamentais de Entropia e Sintropia para o Modelo X Framework"""

import numpy as np

class EntropySyntropyCalculator:
    """Calcula métricas entropicas e sintropicas em diferentes contextos"""
    
    def __init__(self, base_entropy=0.5, base_syntropy=0.5):
        self.base_entropy = base_entropy
        self.base_syntropy = base_syntropy
    
    def calculate_shannon_entropy(self, data):
        """Calcula entropia de Shannon NORMALIZADA para [0,1]"""
        if isinstance(data, np.ndarray):
            data = data.tolist()
        
        if not data or len(data) == 0:
            return 0.0
        
        values, counts = np.unique(data, return_counts=True)
        probabilities = counts / len(data)
        
        # Entropia em bits
        entropy_bits = -np.sum(probabilities * np.log2(probabilities + 1e-15))
        
        # NORMALIZAR para [0,1] dividindo pela entropia máxima possível
        # Para N símbolos únicos, entropia máxima = log2(N)
        num_unique_values = len(values)
        if num_unique_values > 1:
            max_entropy = np.log2(num_unique_values)
            normalized_entropy = entropy_bits / max_entropy
        else:
            normalized_entropy = 0.0  # Apenas 1 valor único = 0 entropia
        
        return max(0.0, min(1.0, normalized_entropy))
    
    def calculate_syntropy(self, data, method="complement"):
        """Calcula sintropia como complemento organizacional da entropia"""
        entropy = self.calculate_shannon_entropy(data)
        
        if method == "complement":
            return max(0.0, 1.0 - entropy)
        elif method == "logistic":
            return 1 / (1 + np.exp(-5 * (0.5 - entropy)))
        else:
            return max(0.0, 1.0 - entropy)
