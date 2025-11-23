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

    # ==================== Testes de Edge Cases ====================

    def test_get_statistics_empty_history(self):
        """Testa estatísticas quando histórico está vazio"""
        # Não executar simulação, histórico vazio
        sim = SimulationEngine()
        stats = sim.get_statistics()

        self.assertEqual(stats['total_steps'], 0)
        self.assertEqual(stats['mean_dilation'], 0)
        self.assertEqual(stats['std_dilation'], 0)

    def test_basic_simulation_fallback(self):
        """Testa que _basic_simulation funciona como fallback"""
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}

        # Usar tipo desconhecido para acionar _basic_simulation
        history = self.sim.run_simulation(initial_state, 'unknown_type')

        # Deve ter gerado histórico (fallback para deterministic)
        self.assertGreater(len(history), 0)

    def test_unknown_simulation_type(self):
        """Testa comportamento com tipo de simulação desconhecido"""
        initial_state = {'entropy': 0.4, 'syntropy': 0.6, 'energy': 1.2}

        history = self.sim.run_simulation(initial_state, 'invalid_type')

        # Deve ainda funcionar (fallback)
        self.assertIsInstance(history, list)
        self.assertGreater(len(history), 0)

    def test_energy_minimum_boundary(self):
        """Testa que energia não cai abaixo do mínimo"""
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 0.15}

        history = self.sim.run_simulation(initial_state, 'deterministic')

        # Energia nunca deve ser menor que 0.1
        for step in history:
            self.assertGreaterEqual(step['state']['energy'], 0.1)

    def test_max_steps_limit_respected(self):
        """Testa que max_steps é respeitado"""
        sim = SimulationEngine(max_steps=50)
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 10.0}

        history = sim.run_simulation(initial_state, 'deterministic')

        # Não deve exceder max_steps
        self.assertLessEqual(len(history), 50)

    def test_entropy_bounds_maintained(self):
        """Testa que entropia permanece entre 0 e 1"""
        initial_state = {'entropy': 0.99, 'syntropy': 0.01, 'energy': 2.0}

        history = self.sim.run_simulation(initial_state, 'deterministic')

        for step in history:
            self.assertGreaterEqual(step['state']['entropy'], 0.0)
            self.assertLessEqual(step['state']['entropy'], 1.0)

    def test_syntropy_bounds_maintained(self):
        """Testa que sintropia permanece entre 0 e 1"""
        initial_state = {'entropy': 0.01, 'syntropy': 0.99, 'energy': 2.0}

        history = self.sim.run_simulation(initial_state, 'deterministic')

        for step in history:
            self.assertGreaterEqual(step['state']['syntropy'], 0.0)
            self.assertLessEqual(step['state']['syntropy'], 1.0)

    def test_initial_state_not_modified(self):
        """Testa que estado inicial não é modificado pela simulação"""
        initial_state = {'entropy': 0.3, 'syntropy': 0.7, 'energy': 1.5}
        original_entropy = initial_state['entropy']
        original_syntropy = initial_state['syntropy']
        original_energy = initial_state['energy']

        self.sim.run_simulation(initial_state, 'deterministic')

        # Estado original não deve ter sido modificado
        self.assertEqual(initial_state['entropy'], original_entropy)
        self.assertEqual(initial_state['syntropy'], original_syntropy)
        self.assertEqual(initial_state['energy'], original_energy)

    def test_custom_dt_parameter(self):
        """Testa que parâmetro dt afeta os tempos registrados"""
        sim = SimulationEngine(dt=0.1, max_steps=100)
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}

        history = sim.run_simulation(initial_state, 'deterministic')

        # Verificar se dt está sendo usado corretamente
        if len(history) > 1:
            time_diff = history[1]['time'] - history[0]['time']
            self.assertAlmostEqual(time_diff, 0.1, places=5)

    def test_history_step_numbering(self):
        """Testa que passos são numerados corretamente"""
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}

        history = self.sim.run_simulation(initial_state, 'deterministic')

        for i, step in enumerate(history):
            self.assertEqual(step['step'], i)

    def test_dilation_calculation_correctness(self):
        """Testa que dilatação é calculada corretamente"""
        initial_state = {'entropy': 0.3, 'syntropy': 0.7, 'energy': 2.0}

        history = self.sim.run_simulation(initial_state, 'deterministic')

        # Verificar primeiro passo (antes de qualquer modificação)
        first_step = history[0]
        expected_dilation = 2.0 * (1.0 + 0.7 - 0.3)  # energy * (1 + syntropy - entropy)
        self.assertAlmostEqual(first_step['dilation'], expected_dilation, places=5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
