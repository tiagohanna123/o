# -*- coding: utf-8 -*-
"""Testes unitários para EntropySyntropyCalculator"""

import sys
sys.path.insert(0, 'src')
import unittest
import numpy as np
from model_x import EntropySyntropyCalculator

class TestEntropySyntropyCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calc = EntropySyntropyCalculator()
    
    def test_shannon_entropy_perfect_random(self):
        """Testa entropia de Shannon para dados perfeitamente aleatórios"""
        # Dados com distribuição uniforme
        data = [0, 1, 0, 1, 0, 1]  # 50% 0, 50% 1
        entropy = self.calc.calculate_shannon_entropy(data)
        self.assertAlmostEqual(entropy, 1.0, places=2)
    
    def test_shannon_entropy_deterministic(self):
        """Testa entropia para dados determinísticos"""
        data = [1, 1, 1, 1, 1, 1]  # 100% 1
        entropy = self.calc.calculate_shannon_entropy(data)
        self.assertAlmostEqual(entropy, 0.0, places=2)
    
    def test_syntropy_complement_method(self):
        """Testa cálculo de sintropia método complemento"""
        # Dados com baixa entropia = alta sintropia
        data = [1, 1, 1, 1, 1]
        entropy = self.calc.calculate_shannon_entropy(data)
        syntropy = self.calc.calculate_syntropy(data, method='complement')
        
        self.assertAlmostEqual(entropy, 0.0, places=2)
        self.assertAlmostEqual(syntropy, 1.0, places=2)
    
    def test_syntropy_high_entropy(self):
        """Testa sintropia para dados com alta entropia"""
        data = [0, 1, 0, 1, 0, 1]  # Máxima entropia
        entropy = self.calc.calculate_shannon_entropy(data)
        syntropy = self.calc.calculate_syntropy(data, method='complement')
        
        self.assertAlmostEqual(entropy, 1.0, places=2)
        self.assertAlmostEqual(syntropy, 0.0, places=2)
    
    def test_edge_cases(self):
        """Testa casos extremos"""
        # Dados vazios devem retornar 0
        empty_data = []
        entropy_empty = self.calc.calculate_shannon_entropy(empty_data)
        self.assertEqual(entropy_empty, 0.0)
        
        # Dados únicos devem retornar 0
        single_data = [5]
        entropy_single = self.calc.calculate_shannon_entropy(single_data)
        self.assertEqual(entropy_single, 0.0)
    
    def test_consistency(self):
        """Testa consistência dos cálculos"""
        # Testa múltiplas vezes com mesmos dados
        data = np.random.choice([0, 1], size=100)
        entropy1 = self.calc.calculate_shannon_entropy(data)
        entropy2 = self.calc.calculate_shannon_entropy(data)
        
        self.assertEqual(entropy1, entropy2)

if __name__ == '__main__':
    unittest.main(verbosity=2)
