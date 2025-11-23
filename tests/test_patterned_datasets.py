# -*- coding: utf-8 -*-
"""Testes unitários para patterned_datasets"""

import sys
sys.path.insert(0, 'src')
import unittest
import numpy as np
from model_x.patterned_datasets import create_patterned_datasets


class TestPatternedDatasets(unittest.TestCase):
    """Testes para o módulo de datasets com padrões"""

    def setUp(self):
        self.datasets = create_patterned_datasets()

    def test_returns_dictionary(self):
        """Testa se retorna um dicionário"""
        self.assertIsInstance(self.datasets, dict)

    def test_contains_expected_datasets(self):
        """Testa se contém os datasets esperados"""
        expected_keys = ['biology_patterned', 'physics_patterned']
        for key in expected_keys:
            self.assertIn(key, self.datasets)

    def test_dataset_structure(self):
        """Testa estrutura de cada dataset"""
        required_keys = ['name', 'description', 'data', 'expected_entropy', 'expected_syntropy']

        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                for key in required_keys:
                    self.assertIn(key, dataset, f"Dataset '{dataset_name}' missing key '{key}'")

    def test_data_length_is_100(self):
        """Testa se cada dataset tem 100 pontos de dados"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertEqual(len(dataset['data']), 100)

    def test_data_is_list(self):
        """Testa se os dados são uma lista"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertIsInstance(dataset['data'], list)

    def test_expected_entropy_in_valid_range(self):
        """Testa se expected_entropy está entre 0 e 1"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertGreaterEqual(dataset['expected_entropy'], 0.0)
                self.assertLessEqual(dataset['expected_entropy'], 1.0)

    def test_expected_syntropy_in_valid_range(self):
        """Testa se expected_syntropy está entre 0 e 1"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertGreaterEqual(dataset['expected_syntropy'], 0.0)
                self.assertLessEqual(dataset['expected_syntropy'], 1.0)

    def test_entropy_syntropy_sum_approximately_one(self):
        """Testa se entropia + sintropia aproxima 1.0"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                total = dataset['expected_entropy'] + dataset['expected_syntropy']
                self.assertAlmostEqual(total, 1.0, places=1)

    def test_biology_pattern_has_valid_data(self):
        """Testa se o dataset biology_patterned tem dados válidos"""
        data = np.array(self.datasets['biology_patterned']['data'])

        # Dados devem ser numéricos e não conter NaN
        self.assertFalse(np.any(np.isnan(data)))
        self.assertFalse(np.any(np.isinf(data)))

        # Dados devem ter variação (não constantes)
        self.assertGreater(np.std(data), 0)

    def test_physics_pattern_has_valid_data(self):
        """Testa se o dataset physics_patterned tem dados válidos"""
        data = np.array(self.datasets['physics_patterned']['data'])

        # Dados devem ser numéricos e não conter NaN
        self.assertFalse(np.any(np.isnan(data)))
        self.assertFalse(np.any(np.isinf(data)))

        # Dados devem ter variação (não constantes)
        self.assertGreater(np.std(data), 0)

    def test_biology_pattern_has_sinusoidal_component(self):
        """Testa se biology_patterned tem componente sinusoidal detectável"""
        data = np.array(self.datasets['biology_patterned']['data'])

        # FFT para detectar componentes de frequência
        fft_result = np.abs(np.fft.fft(data - np.mean(data)))

        # Deve haver picos de frequência (componentes sinusoidais)
        # Ignorar DC component (índice 0)
        max_freq_power = np.max(fft_result[1:len(fft_result)//2])
        self.assertGreater(max_freq_power, 1.0)

    def test_physics_pattern_has_harmonic_components(self):
        """Testa se physics_patterned tem harmônicos detectáveis"""
        data = np.array(self.datasets['physics_patterned']['data'])

        # FFT para detectar componentes de frequência
        fft_result = np.abs(np.fft.fft(data - np.mean(data)))

        # Deve haver múltiplos picos (harmônicos)
        freq_powers = fft_result[1:len(fft_result)//2]
        threshold = np.max(freq_powers) * 0.1  # 10% do pico máximo
        significant_peaks = np.sum(freq_powers > threshold)

        # Deve ter pelo menos 2 picos significativos (fundamental + harmônicos)
        self.assertGreaterEqual(significant_peaks, 2)

    def test_name_is_string(self):
        """Testa se name é uma string"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertIsInstance(dataset['name'], str)
                self.assertGreater(len(dataset['name']), 0)

    def test_description_is_string(self):
        """Testa se description é uma string"""
        for dataset_name, dataset in self.datasets.items():
            with self.subTest(dataset=dataset_name):
                self.assertIsInstance(dataset['description'], str)
                self.assertGreater(len(dataset['description']), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
