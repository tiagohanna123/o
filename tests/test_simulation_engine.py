# -*- coding: utf-8 -*-
"""Testes unitários para SimulationEngine"""

import sys
sys.path.insert(0, 'src')
import unittest
import numpy as np
from model_x import SimulationEngine

class TestSimulationEngine(unittest.TestCase):
    
    def setUp(self):
        self.sim = SimulationEngine(dt=0.01, max_steps=1000)
    
    def test_deterministic_simulation_basic(self):
        """Testa simulação determinística básica"""
        initial_state = {'entropy': 0.3, 'syntropy': 0.7, 'energy': 1.5}
        
        history = self.sim.run_simulation(initial_state, 'deterministic')
        
        # Deve ter gerado histórico
        self.assertGreater(len(history), 0)
        self.assertLessEqual(len(history), 1000)
        
        # Primeiro estado deve ser igual ao inicial
        self.assertEqual(history[0]['state']['entropy'], initial_state['entropy'])
        self.assertEqual(history[0]['state']['syntropy'], initial_state['syntropy'])
        self.assertEqual(history[0]['state']['energy'], initial_state['energy'])
    
    def test_simulation_statistics(self):
        """Testa cálculo de estatísticas"""
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}
        
        history = self.sim.run_simulation(initial_state, 'deterministic')
        stats = self.sim.get_statistics()
        
        # Deve ter estatísticas válidas
        self.assertIn('mean_dilation', stats)
        self.assertIn('std_dilation', stats)
        self.assertIn('total_steps', stats)
        
        # Estatísticas devem ser números válidos
        self.assertGreaterEqual(stats['mean_dilation'], 0)
        self.assertGreaterEqual(stats['std_dilation'], 0)
        self.assertGreater(stats['total_steps'], 0)
    
    def test_different_initial_conditions(self):
        """Testa diferentes condições iniciais"""
        test_cases = [
            {'entropy': 0.1, 'syntropy': 0.9, 'energy': 2.0},
            {'entropy': 0.8, 'syntropy': 0.2, 'energy': 0.5},
            {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}
        ]
        
        for initial_state in test_cases:
            with self.subTest(initial_state=initial_state):
                history = self.sim.run_simulation(initial_state, 'deterministic')
                
                # Deve ter gerado histórico
                self.assertGreater(len(history), 0)
                
                # Energia não deve ser negativa
                for step in history:
                    self.assertGreaterEqual(step['state']['energy'], 0.1)
    
    def test_simulation_convergence(self):
        """Testa se simulação converge"""
        initial_state = {'entropy': 0.6, 'syntropy': 0.4, 'energy': 1.0}
        
        history = self.sim.run_simulation(initial_state, 'deterministic')
        
        # Últimos 10 passos devem ser similares (convergência)
        if len(history) >= 20:
            last_dilations = [h['dilation'] for h in history[-10:]]
            dilation_std = np.std(last_dilations)
            
            # Desvio padrão deve ser pequeno (convergência)
            self.assertLess(dilation_std, 0.1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
