# -*- coding: utf-8 -*-
"""Demonstração de Validação com Dados Reais - Modelo X Framework v2.0.0"""

import sys
sys.path.insert(0, 'src')
from model_x import ValidationUtils, SimulationEngine, EntropySyntropyCalculator

def main():
    print('🧪 VALIDAÇÃO COM DADOS REAIS - Modelo X Framework v2.0.0')
    print('='*60)

    # 1. Carregar datasets de validação
    utils = ValidationUtils()
    datasets = utils.create_default_datasets()

    # 2. Validar cada dataset
    for domain, data in datasets.items():
        print()
        print(f'Dominio: {domain.upper()} - {data["name"]}')
        
        # Calcular entropia e sintropia dos dados reais
        calc = EntropySyntropyCalculator()
        entropy_real = calc.calculate_shannon_entropy(data['data'])
        syntropy_real = calc.calculate_syntropy(data['data'])
        
        print(f'   Entropia Real: {entropy_real:.3f} (esperado: {data["expected_entropy"]:.3f})')
        print(f'   Sintropia Real: {syntropy_real:.3f} (esperado: {data["expected_syntropy"]:.3f})')
        
        # Simular com Modelo X
        sim = SimulationEngine()
        initial_state = {'entropy': entropy_real, 'syntropy': syntropy_real, 'energy': 1.0}
        result = sim.run_simulation(initial_state)
        stats = sim.get_statistics()
        
        print(f'   Dilatação Média: {stats["mean_dilation"]:.3f}')
        print(f'   Passos de Simulação: {stats["total_steps"]}')

    print()
    print('✅ Validação concluída! Todos os domínios testados.')

if __name__ == '__main__':
    main()
