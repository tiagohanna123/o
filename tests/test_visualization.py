# -*- coding: utf-8 -*-
"""Testes unitários para ModelXVisualizer"""

import sys
sys.path.insert(0, 'src')
import unittest
import json
import os
from model_x import ModelXVisualizer, SimulationEngine

class TestModelXVisualizer(unittest.TestCase):
    
    def setUp(self):
        self.viz = ModelXVisualizer()
        self.sim = SimulationEngine()
    
    def test_export_simulation_data(self):
        """Testa exportação de dados de simulação"""
        # Criar dados de teste
        history = self.sim.run_simulation({'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0})
        
        # Exportar dados
        filename = 'test_export.json'
        exported_file = self.viz.export_simulation_data(history, filename)
        
        # Verificar se arquivo foi criado
        self.assertTrue(os.path.exists(exported_file))
        
        # Verificar conteúdo
        with open(exported_file, 'r') as f:
            data = json.load(f)
        
        self.assertIn('time', data)
        self.assertIn('dilation', data)
        self.assertIn('entropy', data)
        self.assertIn('syntropy', data)
        self.assertIn('energy', data)
        
        # Limpar
        if os.path.exists(exported_file):
            os.remove(exported_file)
    
    def test_ascii_plot(self):
        """Testa criação de gráfico ASCII"""
        # Dados simples
        data = [1, 2, 3, 2, 1]
        ascii_chart = self.viz.ascii_plot(data, "Teste ASCII", width=20, height=5)
        
        # Deve conter título e bordas
        self.assertIn("Teste ASCII", ascii_chart)
        self.assertIn("+", ascii_chart)  # Bordas
        self.assertIn("|", ascii_chart)  # Bordas verticais
    
    def test_simulation_summary(self):
        """Testa geração de resumo da simulação"""
        # Criar histórico de teste
        history = [
            {'step': 0, 'time': 0.0, 'state': {'entropy': 0.3, 'syntropy': 0.7, 'energy': 1.5}, 'dilation': 2.1},
            {'step': 1, 'time': 0.1, 'state': {'entropy': 0.31, 'syntropy': 0.69, 'energy': 1.49}, 'dilation': 2.08}
        ]
        
        # Não deve lançar exceção
        try:
            self.viz.print_simulation_summary(history)
            success = True
        except Exception as e:
            success = False
            print(f"Erro: {e}")
        
        self.assertTrue(success)
    
    def test_empty_data_handling(self):
        """Testa tratamento de dados vazios"""
        empty_history = []
        
        # Não deve lançar exceção com dados vazios
        try:
            self.viz.print_simulation_summary(empty_history)
            success = True
        except Exception:
            success = False
        
        self.assertTrue(success)
    
    def test_generate_report(self):
        """Testa geração de relatório"""
        # Criar histórico de teste
        history = self.sim.run_simulation({'entropy': 0.5, 'syntropy': 0.5, 'energy': 1.0})
        
        # Gerar relatório
        report_file = 'test_report.txt'
        report_text = self.viz.generate_report(history, report_file)
        
        # Verificar se arquivo foi criado
        self.assertTrue(os.path.exists(report_file))
        
        # Verificar conteúdo
        self.assertIn("MODELO X FRAMEWORK", report_text)
        self.assertIn("Total de passos", report_text)
        
        # Limpar
        if os.path.exists(report_file):
            os.remove(report_file)

if __name__ == '__main__':
    unittest.main(verbosity=2)
