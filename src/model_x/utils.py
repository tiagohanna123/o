# -*- coding: utf-8 -*-
"""Utilitários e ferramentas de validação para Modelo X Framework - VERSÃO CORRIGIDA"""

import json
import os
import numpy as np
from datetime import datetime

class ValidationUtils:
    """Ferramentas de validação de modelos"""
    
    @staticmethod
    def validate_parameters(entropy, syntropy, energy):
        \"\"\"Valida parâmetros do modelo\"\"\"
        errors = []
        
        if not (0.0 <= float(entropy) <= 1.0):
            errors.append(\"Entropia deve estar entre 0.0 e 1.0\")
        
        if not (0.0 <= float(syntropy) <= 1.0):
            errors.append(\"Sintropia deve estar entre 0.0 e 1.0\")
        
        if float(energy) <= 0.0:
            errors.append(\"Energia deve ser positiva\")
        
        return errors
    
    @staticmethod
    def export_simulation_results(simulation_history, filename):
        \"\"\"Exporta resultados para JSON\"\"\"
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_steps': len(simulation_history),
            'final_state': simulation_history[-1]['state'] if simulation_history else None,
            'statistics': {
                'mean_dilation': np.mean([h['dilation'] for h in simulation_history]) if simulation_history else 0,
                'std_dilation': np.std([h['dilation'] for h in simulation_history]) if simulation_history else 0,
                'max_dilation': np.max([h['dilation'] for h in simulation_history]) if simulation_history else 0,
                'min_dilation': np.min([h['dilation'] for h in simulation_history]) if simulation_history else 0
            },
            'history': simulation_history
        }
        
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f\"✅ Resultados exportados para {filename}\")
        return filename
    
    @staticmethod
    def load_validation_datasets(filename='data/validation_datasets.json'):
        \"\"\"Carrega datasets de validação\"\"\"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f\"⚠️  Arquivo {filename} não encontrado. Criando dataset padrão...\")
            return ValidationUtils.create_default_datasets()
    
    @staticmethod
    def create_default_datasets():
        \"\"\"Cria datasets de validação com padrões DETECTÁVEIS - CORRIGIDO\"\"\"
        np.random.seed(42)
        
        datasets = {
            'finance': {
                'name': 'Série Temporal Financeira (Simulado)',
                'description': 'Dados de volatilidade de mercado com ruído gaussiano',
                'data': (np.cumsum(np.random.normal(0, 0.01, 100)) + 1.0).tolist(),
                'expected_entropy': 0.95,  # Dados gaussianos são altamente aleatórios
                'expected_syntropy': 0.05
            },
            'biology': {
                'name': 'Ritmo Cardíaco com Padrões (Simulado)',
                'description': 'ECG com frequência cardíaca FORTE + ruído leve',
                'data': (1.0 + 
                        0.5 * np.sin(np.linspace(0, 4*np.pi, 100)) +      # Frequência cardíaca
                        0.3 * np.sin(np.linspace(0, 12*np.pi, 100)) +     # Respiração
                        0.1 * np.sin(np.linspace(0, 24*np.pi, 100)) +     # Mayer waves
                        0.05 * np.random.normal(0, 1, 100)).tolist(),     # Ruído mínimo
                'expected_entropy': 0.45,  # Múltiplas frequências = entropia média
                'expected_syntropy': 0.55
            },
            'physics': {
                'name': 'Oscilações com Harmônicos (Simulado)',
                'description': 'Sistema físico com múltiplos harmônicos detectáveis',
                'data': (25 + 
                        6 * np.sin(np.linspace(0, 4*np.pi, 100)) +        # Frequência principal
                        3 * np.sin(np.linspace(0, 8*np.pi, 100)) +        # 2º harmônico  
                        1 * np.sin(np.linspace(0, 12*np.pi, 100)) +       # 3º harmônico
                        0.1 * np.random.normal(0, 1, 100)).tolist(),      # Ruído insignificante
                'expected_entropy': 0.35,  # Harmônicos = estrutura forte
                'expected_syntropy': 0.65
            },
            'network': {
                'name': 'Tráfego de Rede (Simulado)',
                'description': 'Pacotes por segundo com distribuição de Poisson',
                'data': np.random.poisson(50, 100).tolist(),
                'expected_entropy': 0.90,  # Poisson é bastante aleatório
                'expected_syntropy': 0.10
            }
        }
        
        # Salva o arquivo
        os.makedirs('data', exist_ok=True)
        with open('data/validation_datasets.json', 'w', encoding='utf-8') as f:
            json.dump(datasets, f, indent=2, default=str)
        
        return datasets
    
    @staticmethod
    def calculate_validation_metrics(simulation_results, expected_values):
        \"\"\"Calcula métricas de validação\"\"\"
        if not simulation_results or not simulation_results.get('final_state'):
            return {'validation_score': 0, 'error': 'Dados inválidos'}
        
        final_state = simulation_results['final_state']
        
        metrics = {
            'entropy_error': abs(final_state['entropy'] - expected_values['expected_entropy']),
            'syntropy_error': abs(final_state['syntropy'] - expected_values['expected_syntropy']),
            'dilation_stability': simulation_results['statistics']['std_dilation'],
            'convergence_rate': len(simulation_results['history']) / max(simulation_results['statistics']['mean_dilation'], 0.1)
        }
        
        # Score de validação (0-100)
        max_allowed_error = 0.3
        entropy_score = max(0, 100 * (1 - metrics['entropy_error'] / max_allowed_error))
        syntropy_score = max(0, 100 * (1 - metrics['syntropy_error'] / max_allowed_error))
        
        metrics['validation_score'] = (entropy_score + syntropy_score) / 2
        
        return metrics
