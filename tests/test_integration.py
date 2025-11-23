# -*- coding: utf-8 -*-
"""Testes de integração para Modelo X Framework"""

import sys
sys.path.insert(0, 'src')
import unittest
import os
import json
from model_x import (
    EntropySyntropyCalculator,
    EnergyModulationEngine,
    SimulationEngine,
    ModelXVisualizer,
    ValidationUtils,
    EnergyModulatedModel
)
from model_x.patterned_datasets import create_patterned_datasets


class TestCalculatorToSimulationWorkflow(unittest.TestCase):
    """Testes de integração: Calculator → Simulation"""

    def test_calculator_results_feed_simulation(self):
        """Testa fluxo Calculator → Simulation"""
        # 1. Criar dados e calcular métricas
        calculator = EntropySyntropyCalculator()
        data = [1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0, 2.0]

        entropy = calculator.calculate_shannon_entropy(data)
        syntropy = calculator.calculate_syntropy(data)

        # 2. Usar resultados em simulação
        sim = SimulationEngine(max_steps=50)
        initial_state = {
            'entropy': entropy,
            'syntropy': syntropy,
            'energy': 1.0
        }

        history = sim.run_simulation(initial_state, 'deterministic')

        # Verificações
        self.assertGreater(len(history), 0)
        self.assertEqual(history[0]['state']['entropy'], entropy)
        self.assertEqual(history[0]['state']['syntropy'], syntropy)

    def test_calculator_with_different_data_types(self):
        """Testa calculadora com diferentes tipos de dados"""
        calculator = EntropySyntropyCalculator()

        # Lista de floats
        data_float = [1.5, 2.5, 3.5, 4.5, 5.5]
        entropy1 = calculator.calculate_shannon_entropy(data_float)

        # Lista de inteiros
        data_int = [1, 2, 3, 4, 5]
        entropy2 = calculator.calculate_shannon_entropy(data_int)

        # Ambos devem retornar valores válidos
        self.assertGreaterEqual(entropy1, 0.0)
        self.assertLessEqual(entropy1, 1.0)
        self.assertGreaterEqual(entropy2, 0.0)
        self.assertLessEqual(entropy2, 1.0)


class TestSimulationToVisualizationWorkflow(unittest.TestCase):
    """Testes de integração: Simulation → Visualization"""

    def setUp(self):
        self.sim = SimulationEngine(max_steps=50)
        self.viz = ModelXVisualizer()
        self.test_files = []

    def tearDown(self):
        # Limpar arquivos de teste criados
        for f in self.test_files:
            if os.path.exists(f):
                os.remove(f)

    def test_simulation_to_visualization_export(self):
        """Testa fluxo Simulation → Visualization export"""
        # 1. Executar simulação
        initial_state = {'entropy': 0.4, 'syntropy': 0.6, 'energy': 1.5}
        history = self.sim.run_simulation(initial_state, 'deterministic')

        # 2. Exportar para visualização (export_simulation_data takes history and filename)
        filename = 'test_integration_export.json'
        self.test_files.append(filename)

        self.viz.export_simulation_data(history, filename)

        # Verificações
        self.assertTrue(os.path.exists(filename))
        with open(filename, 'r') as f:
            data = json.load(f)

        # export_simulation_data exports time, dilation, entropy, syntropy, energy arrays
        self.assertIn('time', data)
        self.assertIn('dilation', data)
        self.assertEqual(len(data['time']), len(history))

    def test_simulation_to_ascii_plot(self):
        """Testa fluxo Simulation → ASCII plot"""
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}
        history = self.sim.run_simulation(initial_state, 'deterministic')

        # Extrair dados para plot
        values = [h['dilation'] for h in history]

        # Gerar ASCII plot
        plot = self.viz.ascii_plot(values, title="Dilation", width=40, height=10)

        # Verificações
        self.assertIsInstance(plot, str)
        self.assertGreater(len(plot), 0)
        self.assertIn('Dilation', plot)


class TestFullValidationPipeline(unittest.TestCase):
    """Testes de integração: Pipeline completo de validação"""

    def setUp(self):
        self.utils = ValidationUtils()
        self.calculator = EntropySyntropyCalculator()
        self.sim = SimulationEngine(max_steps=50)
        self.test_files = []

    def tearDown(self):
        for f in self.test_files:
            if os.path.exists(f):
                os.remove(f)

    def test_full_pipeline_with_default_datasets(self):
        """Testa pipeline completo com datasets padrão"""
        # 1. Criar datasets
        datasets = self.utils.create_default_datasets()

        # 2. Para cada dataset, calcular métricas e simular
        for name, dataset in datasets.items():
            with self.subTest(dataset=name):
                # Calcular entropia/sintropia real
                data = dataset['data']
                entropy = self.calculator.calculate_shannon_entropy(data)
                syntropy = self.calculator.calculate_syntropy(data)

                # Simular
                initial_state = {
                    'entropy': entropy,
                    'syntropy': syntropy,
                    'energy': 1.0
                }
                history = self.sim.run_simulation(initial_state, 'deterministic')

                # Verificações básicas
                self.assertGreater(len(history), 0)
                self.assertGreaterEqual(entropy, 0.0)
                self.assertLessEqual(entropy, 1.0)

    def test_validation_metrics_calculation(self):
        """Testa cálculo de métricas de validação no pipeline"""
        # Simular
        initial_state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}
        history = self.sim.run_simulation(initial_state, 'deterministic')
        stats = self.sim.get_statistics()

        # Preparar resultados
        simulation_results = {
            'final_state': history[-1]['state'] if history else {},
            'statistics': stats,
            'history': history
        }

        expected_values = {
            'expected_entropy': 0.5,
            'expected_syntropy': 0.5
        }

        # Calcular métricas
        metrics = self.utils.calculate_validation_metrics(
            simulation_results, expected_values
        )

        # Verificações
        self.assertIn('entropy_error', metrics)
        self.assertIn('syntropy_error', metrics)
        self.assertIn('validation_score', metrics)
        self.assertGreaterEqual(metrics['validation_score'], 0)
        self.assertLessEqual(metrics['validation_score'], 100)


class TestPatternedDataValidation(unittest.TestCase):
    """Testes de integração: Validação com dados padronizados"""

    def setUp(self):
        self.calculator = EntropySyntropyCalculator()
        self.datasets = create_patterned_datasets()

    def test_patterned_datasets_entropy_calculation(self):
        """Testa cálculo de entropia em datasets padronizados"""
        for name, dataset in self.datasets.items():
            with self.subTest(dataset=name):
                data = dataset['data']
                calculated_entropy = self.calculator.calculate_shannon_entropy(data)

                # Entropia calculada deve estar em range válido [0, 1]
                self.assertGreaterEqual(calculated_entropy, 0.0)
                self.assertLessEqual(calculated_entropy, 1.0)

                # Verificar que entropia é um número válido (não NaN ou Inf)
                import math
                self.assertFalse(math.isnan(calculated_entropy))
                self.assertFalse(math.isinf(calculated_entropy))

    def test_patterned_datasets_syntropy_calculation(self):
        """Testa cálculo de sintropia em datasets padronizados"""
        for name, dataset in self.datasets.items():
            with self.subTest(dataset=name):
                data = dataset['data']
                calculated_syntropy = self.calculator.calculate_syntropy(data)

                # Sintropia deve estar em range válido
                self.assertGreaterEqual(calculated_syntropy, 0.0)
                self.assertLessEqual(calculated_syntropy, 1.0)

    def test_entropy_syntropy_relationship(self):
        """Testa relação entre entropia e sintropia calculadas"""
        for name, dataset in self.datasets.items():
            with self.subTest(dataset=name):
                data = dataset['data']
                entropy = self.calculator.calculate_shannon_entropy(data)
                syntropy = self.calculator.calculate_syntropy(data)

                # Sintropia (método complement) deve ser aproximadamente 1 - entropy
                expected_syntropy = 1.0 - entropy
                self.assertAlmostEqual(syntropy, expected_syntropy, places=5)


class TestEnergyModulationIntegration(unittest.TestCase):
    """Testes de integração: Energy Modulation"""

    def setUp(self):
        self.calculator = EntropySyntropyCalculator()
        self.modulator = EnergyModulationEngine()

    def test_calculator_to_modulation(self):
        """Testa fluxo Calculator → EnergyModulation"""
        # Calcular métricas
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        entropy = self.calculator.calculate_shannon_entropy(data)
        syntropy = self.calculator.calculate_syntropy(data)
        energy = 1.0

        # Modular energia - returns tuple (f_E * energy, g_S * energy, (alpha, beta, gamma))
        result = self.modulator.modulate_energy(
            entropy, syntropy, energy, 'adaptive'
        )

        # Verificações - result is a tuple of 3 elements
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 3)
        modulated_f, modulated_g, params = result
        self.assertGreater(float(modulated_f), 0)
        self.assertGreater(float(modulated_g), 0)

    def test_different_modulation_types(self):
        """Testa diferentes tipos de modulação"""
        entropy = 0.5
        syntropy = 0.5
        energy = 1.0

        # Testar todos os tipos - each returns tuple (f_E*energy, g_S*energy, params)
        adaptive = self.modulator.modulate_energy(
            entropy, syntropy, energy, 'adaptive'
        )
        conservative = self.modulator.modulate_energy(
            entropy, syntropy, energy, 'conservative'
        )
        basic = self.modulator.modulate_energy(
            entropy, syntropy, energy, 'basic'
        )

        # Todos devem retornar tuplas de 3 elementos
        for result in [adaptive, conservative, basic]:
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 3)
            modulated_f, modulated_g, params = result
            self.assertGreater(float(modulated_f), 0)
            self.assertGreater(float(modulated_g), 0)


class TestLegacyModelIntegration(unittest.TestCase):
    """Testes de integração: EnergyModulatedModel (legacy)"""

    def test_legacy_model_full_workflow(self):
        """Testa workflow completo usando modelo legado"""
        # Criar modelo
        model = EnergyModulatedModel(entropy=0.4, syntropy=0.6, energy=1.5)

        # Calcular dilatação
        dilation = model.compute_temporal_dilation()
        self.assertIsInstance(dilation, (int, float))

        # Calcular modulação
        f_E, g_S = model.compute_modulation()
        self.assertIsInstance(f_E, (int, float))
        self.assertIsInstance(g_S, (int, float))

        # Simular
        trajectory = model.simulate(steps=50)
        self.assertEqual(len(trajectory), 50)

        # Verificar consistência
        for point in trajectory:
            self.assertAlmostEqual(point['dilation'], dilation, places=5)

    def test_legacy_model_with_new_components(self):
        """Testa modelo legado junto com novos componentes"""
        # Usar calculadora para obter parâmetros
        calculator = EntropySyntropyCalculator()
        data = [1, 2, 3, 2, 1, 2, 3, 2, 1]
        entropy = calculator.calculate_shannon_entropy(data)
        syntropy = calculator.calculate_syntropy(data)

        # Criar modelo legado com parâmetros calculados
        model = EnergyModulatedModel(
            entropy=entropy,
            syntropy=syntropy,
            energy=1.0
        )

        # Executar
        trajectory = model.simulate(steps=20)

        # Verificações
        self.assertEqual(len(trajectory), 20)
        self.assertGreater(trajectory[0]['dilation'], 0)


class TestCrossModuleDataConsistency(unittest.TestCase):
    """Testes de consistência de dados entre módulos"""

    def test_state_dict_consistency(self):
        """Testa que formato de estado é consistente entre módulos"""
        # Estado padrão
        state = {'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0}

        # SimulationEngine deve aceitar e preservar formato
        sim = SimulationEngine(max_steps=10)
        history = sim.run_simulation(state.copy(), 'deterministic')

        # Verificar que estrutura é preservada
        for step in history:
            self.assertIn('entropy', step['state'])
            self.assertIn('syntropy', step['state'])
            self.assertIn('energy', step['state'])

    def test_data_types_consistency(self):
        """Testa consistência de tipos de dados"""
        calculator = EntropySyntropyCalculator()
        data = [1.0, 2.0, 3.0, 4.0, 5.0]

        entropy = calculator.calculate_shannon_entropy(data)
        syntropy = calculator.calculate_syntropy(data)

        # Verificar tipos
        self.assertIsInstance(entropy, float)
        self.assertIsInstance(syntropy, float)

        # Usar em simulação
        sim = SimulationEngine(max_steps=10)
        state = {'entropy': entropy, 'syntropy': syntropy, 'energy': 1.0}
        history = sim.run_simulation(state, 'deterministic')

        # Verificar tipos mantidos
        for step in history:
            self.assertIsInstance(step['state']['entropy'], float)
            self.assertIsInstance(step['state']['syntropy'], float)
            self.assertIsInstance(step['state']['energy'], float)


if __name__ == '__main__':
    unittest.main(verbosity=2)
