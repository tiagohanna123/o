# -*- coding: utf-8 -*-
"""Testes unitários para ValidationUtils"""

import sys
sys.path.insert(0, 'src')
import unittest
import json
import os
from model_x import ValidationUtils

class TestValidationUtils(unittest.TestCase):
    
    def setUp(self):
        self.utils = ValidationUtils()
    
    def test_validate_parameters_valid(self):
        """Testa validação de parâmetros válidos"""
        errors = self.utils.validate_parameters(0.5, 0.5, 1.0)
        self.assertEqual(len(errors), 0)
    
    def test_validate_parameters_invalid_entropy(self):
        """Testa validação de entropia inválida"""
        errors = self.utils.validate_parameters(1.5, 0.5, 1.0)  # Entropia > 1.0
        self.assertGreater(len(errors), 0)
        self.assertTrue(any('Entropia' in error for error in errors))
    
    def test_validate_parameters_invalid_syntropy(self):
        """Testa validação de sintropia inválida"""
        errors = self.utils.validate_parameters(0.5, -0.1, 1.0)  # Sintropia < 0
        self.assertGreater(len(errors), 0)
        self.assertTrue(any('Sintropia' in error for error in errors))
    
    def test_validate_parameters_invalid_energy(self):
        """Testa validação de energia inválida"""
        errors = self.utils.validate_parameters(0.5, 0.5, -1.0)  # Energia < 0
        self.assertGreater(len(errors), 0)
        self.assertTrue(any('Energia' in error for error in errors))
    
    def test_create_default_datasets(self):
        """Testa criação de datasets padrão"""
        datasets = self.utils.create_default_datasets()
        
        # Deve criar datasets conhecidos
        self.assertIn('finance', datasets)
        self.assertIn('biology', datasets)
        self.assertIn('physics', datasets)
        self.assertIn('network', datasets)
        
        # Cada dataset deve ter estrutura correta
        for name, dataset in datasets.items():
            self.assertIn('name', dataset)
            self.assertIn('data', dataset)
            self.assertIn('expected_entropy', dataset)
            self.assertIn('expected_syntropy', dataset)
            
            # Valores esperados devem ser entre 0 e 1
            self.assertGreaterEqual(dataset['expected_entropy'], 0.0)
            self.assertLessEqual(dataset['expected_entropy'], 1.0)
            self.assertGreaterEqual(dataset['expected_syntropy'], 0.0)
            self.assertLessEqual(dataset['expected_syntropy'], 1.0)
    
    def test_export_simulation_results(self):
        """Testa exportação de resultados"""
        # Dados de teste
        simulation_history = [
            {'step': 0, 'time': 0.0, 'state': {'entropy': 0.3, 'syntropy': 0.7, 'energy': 1.5}, 'dilation': 2.1},
            {'step': 1, 'time': 0.1, 'state': {'entropy': 0.31, 'syntropy': 0.69, 'energy': 1.49}, 'dilation': 2.08}
        ]
        
        # Exportar
        filename = 'test_results.json'
        self.utils.export_simulation_results(simulation_history, filename)
        
        # Verificar arquivo
        self.assertTrue(os.path.exists(filename))
        
        # Verificar conteúdo
        with open(filename, 'r') as f:
            results = json.load(f)
        
        self.assertIn('timestamp', results)
        self.assertIn('total_steps', results)
        self.assertIn('final_state', results)
        self.assertIn('statistics', results)
        
        # Limpar
        if os.path.exists(filename):
            os.remove(filename)
    
    def test_calculate_validation_metrics(self):
        """Testa cálculo de métricas de validação"""
        simulation_results = {
            'final_state': {'entropy': 0.6, 'syntropy': 0.6},
            'statistics': {'std_dilation': 0.1, 'mean_dilation': 2.0},
            'history': [{'step': i} for i in range(100)]
        }
        
        expected_values = {
            'expected_entropy': 0.5,
            'expected_syntropy': 0.7
        }
        
        metrics = self.utils.calculate_validation_metrics(simulation_results, expected_values)
        
        # Verificar estrutura
        self.assertIn('entropy_error', metrics)
        self.assertIn('syntropy_error', metrics)
        self.assertIn('validation_score', metrics)
        
        # Scores devem estar entre 0 e 100
        self.assertGreaterEqual(metrics['validation_score'], 0)
        self.assertLessEqual(metrics['validation_score'], 100)

if __name__ == '__main__':
    unittest.main(verbosity=2)
