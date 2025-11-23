# -*- coding: utf-8 -*-
"""Testes unitários para EnergyModulatedModel"""

import sys
sys.path.insert(0, 'src')
import unittest
from model_x import EnergyModulatedModel


class TestEnergyModulatedModel(unittest.TestCase):
    """Testes para a classe EnergyModulatedModel"""

    def setUp(self):
        self.model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=1.0)

    # ==================== Testes de Inicialização ====================

    def test_basic_initialization(self):
        """Testa inicialização básica com valores padrão"""
        model = EnergyModulatedModel()
        self.assertEqual(model.entropy, 0.5)
        self.assertEqual(model.syntropy, 0.5)
        self.assertEqual(model.energy, 1.0)

    def test_custom_initialization(self):
        """Testa inicialização com valores customizados"""
        model = EnergyModulatedModel(entropy=0.3, syntropy=0.7, energy=2.0)
        self.assertEqual(model.entropy, 0.3)
        self.assertEqual(model.syntropy, 0.7)
        self.assertEqual(model.energy, 2.0)

    def test_parameter_clamping_negative_entropy(self):
        """Testa que entropia negativa é clampada para 0"""
        model = EnergyModulatedModel(entropy=-0.5, syntropy=0.5, energy=1.0)
        self.assertEqual(model.entropy, 0.0)

    def test_parameter_clamping_negative_syntropy(self):
        """Testa que sintropia negativa é clampada para 0"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=-0.3, energy=1.0)
        self.assertEqual(model.syntropy, 0.0)

    def test_parameter_clamping_low_energy(self):
        """Testa que energia muito baixa é clampada para 0.1"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=0.05)
        self.assertEqual(model.energy, 0.1)

    def test_parameter_clamping_negative_energy(self):
        """Testa que energia negativa é clampada para 0.1"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=-1.0)
        self.assertEqual(model.energy, 0.1)

    def test_parameter_clamping_zero_energy(self):
        """Testa que energia zero é clampada para 0.1"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=0.0)
        self.assertEqual(model.energy, 0.1)

    def test_parameters_converted_to_float(self):
        """Testa que parâmetros inteiros são convertidos para float"""
        model = EnergyModulatedModel(entropy=1, syntropy=0, energy=2)
        self.assertIsInstance(model.entropy, float)
        self.assertIsInstance(model.syntropy, float)
        self.assertIsInstance(model.energy, float)

    # ==================== Testes de compute_temporal_dilation ====================

    def test_temporal_dilation_balanced(self):
        """Testa dilatação temporal com entropia e sintropia balanceadas"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=1.0)
        dilation = model.compute_temporal_dilation()
        # balance = 0.5 - 0.5 = 0, dilation = 1.0 * (1.0 + 0) = 1.0
        self.assertAlmostEqual(dilation, 1.0, places=5)

    def test_temporal_dilation_syntropy_dominant(self):
        """Testa dilatação temporal com sintropia dominante"""
        model = EnergyModulatedModel(entropy=0.2, syntropy=0.8, energy=1.0)
        dilation = model.compute_temporal_dilation()
        # balance = 0.8 - 0.2 = 0.6, dilation = 1.0 * (1.0 + 0.6) = 1.6
        self.assertAlmostEqual(dilation, 1.6, places=5)

    def test_temporal_dilation_entropy_dominant(self):
        """Testa dilatação temporal com entropia dominante"""
        model = EnergyModulatedModel(entropy=0.9, syntropy=0.1, energy=1.0)
        dilation = model.compute_temporal_dilation()
        # balance = 0.1 - 0.9 = -0.8, dilation = 1.0 * (1.0 - 0.8) = 0.2
        self.assertAlmostEqual(dilation, 0.2, places=5)

    def test_temporal_dilation_with_high_energy(self):
        """Testa dilatação temporal com energia alta"""
        model = EnergyModulatedModel(entropy=0.5, syntropy=0.5, energy=3.0)
        dilation = model.compute_temporal_dilation()
        # balance = 0, dilation = 3.0 * (1.0 + 0) = 3.0
        self.assertAlmostEqual(dilation, 3.0, places=5)

    def test_temporal_dilation_combined_effect(self):
        """Testa efeito combinado de energia e balance"""
        model = EnergyModulatedModel(entropy=0.3, syntropy=0.7, energy=2.0)
        dilation = model.compute_temporal_dilation()
        # balance = 0.7 - 0.3 = 0.4, dilation = 2.0 * (1.0 + 0.4) = 2.8
        self.assertAlmostEqual(dilation, 2.8, places=5)

    # ==================== Testes de compute_modulation ====================

    def test_compute_modulation_default_params(self):
        """Testa modulação com parâmetros padrão"""
        f_E, g_S = self.model.compute_modulation()
        # alpha=0.3, beta=0.7, gamma=1.5
        # f_E = 1.0 + 0.3 * (0.5 / 1.0) = 1.15
        # g_S = 1.0 + 0.7 * (0.5 / 1.0)^1.5 = 1.0 + 0.7 * 0.3536 ≈ 1.247
        self.assertAlmostEqual(f_E, 1.15, places=3)
        self.assertGreater(g_S, 1.0)

    def test_compute_modulation_custom_alpha(self):
        """Testa modulação com alpha customizado"""
        f_E, g_S = self.model.compute_modulation(alpha=0.5)
        # f_E = 1.0 + 0.5 * (0.5 / 1.0) = 1.25
        self.assertAlmostEqual(f_E, 1.25, places=3)

    def test_compute_modulation_custom_beta(self):
        """Testa modulação com beta customizado"""
        f_E, g_S = self.model.compute_modulation(beta=1.0)
        # g_S = 1.0 + 1.0 * (0.5)^1.5
        self.assertGreater(g_S, 1.0)

    def test_compute_modulation_custom_gamma(self):
        """Testa modulação com gamma customizado"""
        f_E1, g_S1 = self.model.compute_modulation(gamma=1.0)
        f_E2, g_S2 = self.model.compute_modulation(gamma=2.0)
        # gamma maior deve resultar em g_S diferente quando syntropy/energy < 1
        self.assertNotAlmostEqual(g_S1, g_S2, places=3)

    def test_compute_modulation_zero_entropy(self):
        """Testa modulação com entropia zero"""
        model = EnergyModulatedModel(entropy=0.0, syntropy=1.0, energy=1.0)
        f_E, g_S = model.compute_modulation()
        # f_E = 1.0 + 0.3 * (0.0 / 1.0) = 1.0
        self.assertAlmostEqual(f_E, 1.0, places=3)

    def test_compute_modulation_returns_tuple(self):
        """Testa que compute_modulation retorna tupla de dois valores"""
        result = self.model.compute_modulation()
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

    # ==================== Testes de simulate ====================

    def test_simulate_returns_list(self):
        """Testa que simulate retorna uma lista"""
        trajectory = self.model.simulate()
        self.assertIsInstance(trajectory, list)

    def test_simulate_default_steps(self):
        """Testa simulação com número padrão de passos"""
        trajectory = self.model.simulate()
        self.assertEqual(len(trajectory), 100)

    def test_simulate_custom_steps(self):
        """Testa simulação com número customizado de passos"""
        trajectory = self.model.simulate(steps=50)
        self.assertEqual(len(trajectory), 50)

    def test_simulate_trajectory_structure(self):
        """Testa estrutura de cada ponto da trajetória"""
        trajectory = self.model.simulate(steps=10)
        for point in trajectory:
            self.assertIn('step', point)
            self.assertIn('time', point)
            self.assertIn('dilation', point)

    def test_simulate_step_indices(self):
        """Testa se os índices dos passos estão corretos"""
        trajectory = self.model.simulate(steps=10)
        for i, point in enumerate(trajectory):
            self.assertEqual(point['step'], i)

    def test_simulate_time_progression(self):
        """Testa progressão do tempo"""
        dt = 0.01
        trajectory = self.model.simulate(steps=10, dt=dt)
        for i, point in enumerate(trajectory):
            expected_time = i * dt
            self.assertAlmostEqual(point['time'], expected_time, places=5)

    def test_simulate_custom_dt(self):
        """Testa simulação com dt customizado"""
        trajectory = self.model.simulate(steps=5, dt=0.1)
        self.assertAlmostEqual(trajectory[1]['time'], 0.1, places=5)
        self.assertAlmostEqual(trajectory[2]['time'], 0.2, places=5)

    def test_simulate_dilation_values(self):
        """Testa que valores de dilatação são consistentes"""
        trajectory = self.model.simulate(steps=10)
        expected_dilation = self.model.compute_temporal_dilation()
        for point in trajectory:
            self.assertAlmostEqual(point['dilation'], expected_dilation, places=5)

    def test_simulate_single_step(self):
        """Testa simulação com um único passo"""
        trajectory = self.model.simulate(steps=1)
        self.assertEqual(len(trajectory), 1)
        self.assertEqual(trajectory[0]['step'], 0)

    def test_simulate_large_number_of_steps(self):
        """Testa simulação com muitos passos"""
        trajectory = self.model.simulate(steps=1000)
        self.assertEqual(len(trajectory), 1000)


if __name__ == '__main__':
    unittest.main(verbosity=2)
