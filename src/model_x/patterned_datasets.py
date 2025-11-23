# -*- coding: utf-8 -*-
"""Dados com Padrões Reais Detectáveis - Modelo X Framework"""

import numpy as np

def create_patterned_datasets():
    """Cria dados com padrões que realmente reduzem entropia"""

    datasets = {
        'biology_patterned': {
            'name': 'Ritmo Cardíaco com Padrões (Simulado)',
            'description': 'ECG com múltiplas frequências detectáveis',
            'data': (1.0 +
                    0.4 * np.sin(np.linspace(0, 4*np.pi, 100)) +      # Frequência cardíaca
                    0.3 * np.sin(np.linspace(0, 12*np.pi, 100)) +     # Respiração
                    0.1 * np.sin(np.linspace(0, 24*np.pi, 100)) +     # Mayer waves
                    0.05 * np.random.normal(0, 1, 100)).tolist(),     # Ruído mínimo
            'expected_entropy': 0.45,  # Múltiplas frequências = entropia média
            'expected_syntropy': 0.55
        },
        'physics_patterned': {
            'name': 'Oscilações com Harmônicos (Simulado)',
            'description': 'Sistema físico com múltiplos harmônicos',
            'data': (25 +
                    6 * np.sin(np.linspace(0, 4*np.pi, 100)) +        # Frequência principal
                    3 * np.sin(np.linspace(0, 8*np.pi, 100)) +        # 2º harmônico
                    1 * np.sin(np.linspace(0, 12*np.pi, 100)) +       # 3º harmônico
                    0.1 * np.random.normal(0, 1, 100)).tolist(),      # Ruído insignificante
            'expected_entropy': 0.35,  # Harmônicos = estrutura forte
            'expected_syntropy': 0.65
        }
    }

    return datasets
