# -*- coding: utf-8 -*-
"""Testes unitários para EnergyModulationEngine"""

import sys
sys.path.insert(0, 'src')
import unittest
import numpy as np
from model_x import EnergyModulationEngine

class TestEnergyModulationEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = EnergyModulationEngine()
    
    def test_adaptive_modulation_equilibrium(self):
        """Testa modulação quando entropia = sintropia"""
        entropy = 0.5
        syntropy = 0.5
        energy = 1.0
        
        e_mod, s_mod, params = self.engine.modulate_energy(entropy, syntropy, energy, 'adaptive')
        
        # Quando E=S, balance=0, então alpha=0.3, beta=0.7 (valores base)
        self.assertAlmostEqual(params[0], 0.3, places=1)
        self.assertAlmostEqual(params[1], 0.7, places=1)
    
    def test_adaptive_modulation_syntropy_dominant(self):
        """Testa modulação quando sintropia > entropia"""
        entropy = 0.3
        syntropy = 0.7
        energy = 1.0
        
        e_mod, s_mod, params = self.engine.modulate_energy(entropy, syntropy, energy, 'adaptive')
        
        # Sintropia dominante deve aumentar ambos os fatores
        self.assertGreater(e_mod, energy)
        self.assertGreater(s_mod, energy)
    
    def test_conservative_modulation(self):
        """Testa modulação conservativa"""
        entropy = 0.5
        syntropy = 0.5
        energy = 1.0
        
        e_mod, s_mod, params = self.engine.modulate_energy(entropy, syntropy, energy, 'conservative')
        
        # Deve manter energia estável (com pequena dissipação)
        self.assertLess(e_mod, energy)
        self.assertLess(s_mod, energy)
        self.assertEqual(params[2], 1.0)  # gamma = 1.0
    
    def test_parameter_ranges(self):
        """Testa se parâmetros estão dentro dos ranges válidos"""
        for entropy in [0.1, 0.5, 0.9]:
            for syntropy in [0.1, 0.5, 0.9]:
                for energy in [0.5, 1.0, 2.0]:
                    e_mod, s_mod, params = self.engine.modulate_energy(entropy, syntropy, energy)
                    
                    # Resultados devem ser positivos
                    self.assertGreater(e_mod, 0)
                    self.assertGreater(s_mod, 0)
                    
                    # Parâmetros devem ser tupla com 3 elementos
                    self.assertEqual(len(params), 3)

if __name__ == '__main__':
    unittest.main(verbosity=2)
