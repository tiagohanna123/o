# -*- coding: utf-8 -*-
"""Ferramentas de Visualização para Modelo X Framework - Versão Sem Dependências"""

import os
import json
from datetime import datetime

class ModelXVisualizer:
    """Cria visualizações texto e exporta dados para plotagem externa"""
    
    def __init__(self):
        self.data_export = []
    
    def export_simulation_data(self, simulation_history, filename='simulation_data.json'):
        """Exporta dados da simulação para visualização externa"""
        export_data = {
            'time': [h['time'] for h in simulation_history],
            'dilation': [h['dilation'] for h in simulation_history],
            'entropy': [h['state']['entropy'] for h in simulation_history],
            'syntropy': [h['state']['syntropy'] for h in simulation_history],
            'energy': [h['state']['energy'] for h in simulation_history]
        }
        
        # Usar caminho absoluto e garantir diretório
        full_path = os.path.abspath(filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Dados exportados para {filename}")
        return filename
    
    def ascii_plot(self, data, title="Gráfico ASCII", width=60, height=15):
        """Cria gráfico ASCII simples"""
        if not data:
            return "Sem dados"
        
        # Normalizar dados para 0-altura
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            normalized = [height//2] * len(data)
        else:
            normalized = [int((val - min_val) / (max_val - min_val) * (height-1)) for val in data]
        
        # Criar grid
        grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Plotar pontos
        for i, val in enumerate(normalized):
            x = int(i * (width-1) / (len(data)-1)) if len(data) > 1 else 0
            y = height - 1 - val
            if 0 <= y < height and 0 <= x < width:
                grid[y][x] = '*'
        
        # Construir string
        result = f"\n{title}\n"
        result += f"Min: {min_val:.3f} | Max: {max_val:.3f}\n"
        result += '+' + '-'*width + '+\n'
        
        for row in grid:
            result += '|' + ''.join(row) + '|\n'
        
        result += '+' + '-'*width + '+\n'
        return result
    
    def print_simulation_summary(self, simulation_history):
        """Imprime resumo da simulação"""
        if not simulation_history:
            print("⚠️  Sem dados de simulação")
            return
        
        # Extrair dados
        dilations = [h['dilation'] for h in simulation_history]
        entropies = [h['state']['entropy'] for h in simulation_history]
        syntropies = [h['state']['syntropy'] for h in simulation_history]
        
        print("\n" + "="*60)
        print("📊 RESUMO DA SIMULAÇÃO")
        print("="*60)
        
        print(f"📈 Dilatação Temporal:")
        print(f"   Média: {sum(dilations)/len(dilations):.4f}")
        print(f"   Desvio: {(max(dilations)-min(dilations)):.4f}")
        print(f"   Min/Max: {min(dilations):.4f} / {max(dilations):.4f}")
        
        print(f"\n🧮 Entropia:")
        print(f"   Média: {sum(entropies)/len(entropies):.4f}")
        print(f"   Final: {entropies[-1]:.4f}")
        
        print(f"\n🎯 Sintropia:")
        print(f"   Média: {sum(syntropies)/len(syntropies):.4f}")
        print(f"   Final: {syntropies[-1]:.4f}")
        
        print(f"\n📊 Balanço Final: {syntropies[-1] - entropies[-1]:.4f}")
        print("="*60)
        
        # Plot ASCII da dilatação
        print("\n📈 Gráfico ASCII - Dilatação Temporal:")
        ascii_chart = self.ascii_plot(dilations, "τ/τ₀ ao longo do tempo")
        print(ascii_chart)
    
    def generate_report(self, domains_data, output_file='validation_report.txt'):
        """Gera relatório de validação para múltiplos domínios"""
        report = []
        report.append("MODELO X FRAMEWORK - RELATÓRIO DE VALIDAÇÃO")
        report.append("="*50)
        report.append(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total de domínios: {len(domains_data)}")
        
        for domain_data in domains_data:
            report.append(f"\nDomínio: {domain_data['domain'].upper()}")
            report.append(f"  Entropia Real: {domain_data['entropy_real']:.3f}")
            report.append(f"  Sintropia Real: {domain_data['syntropy_real']:.3f}")
            report.append(f"  Dilatação Média: {domain_data['mean_dilation']:.3f}")
            report.append(f"  Score de Validação: {domain_data['validation_score']:.1f}/100")
            report.append(f"  Status: {domain_data['status']}")
        
        report.append(f"\nMÉDIA GERAL: {sum(d['validation_score'] for d in domains_data)/len(domains_data):.1f}/100")
        
        report_text = '\n'.join(report)
        
        # Garantir diretório
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"✅ Relatório salvo em {output_file}")
        return report_text
