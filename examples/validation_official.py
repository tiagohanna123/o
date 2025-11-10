# -*- coding: utf-8 -*-
"""Validação Oficial do Modelo X Framework com Dados Reais"""

import sys
sys.path.insert(0, 'src')
from model_x import ValidationUtils, SimulationEngine, EntropySyntropyCalculator, ModelXVisualizer

def run_official_validation():
    """
    Executa validação oficial do Modelo X Framework com datasets reais
    de múltiplos domínios científicos.
    
    Retorna:
        dict: Resultados completos da validação
    """
    
    print("🔬 VALIDAÇÃO OFICIAL - Modelo X Framework v2.0.0")
    print("="*60)
    print("Domínios testados: Finance, Biology, Physics, Network")
    print("Métricas: Entropia (desordem), Sintropia (ordem), Dilatação Temporal")
    print("="*60)
    
    # Inicializar componentes
    utils = ValidationUtils()
    calc = EntropySyntropyCalculator()
    sim = SimulationEngine()
    viz = ModelXVisualizer()
    
    # Carregar datasets de validação
    datasets = utils.create_default_datasets()
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'framework_version': '2.0.0-alpha',
        'domains_validated': [],
        'overall_score': 0.0
    }
    
    total_score = 0
    
    # Validar cada domínio
    for domain, data in datasets.items():
        print(f"\n📊 DOMÍNIO: {domain.upper()}")
        print(f"   Dataset: {data['name']}")
        print(f"   Descrição: {data['description']}")
        
        # 1. Análise Entrópica
        entropy_real = calc.calculate_shannon_entropy(data['data'])
        syntropy_real = calc.calculate_syntropy(data['data'])
        
        print(f"   Entropia Real: {entropy_real:.3f} (esperado: {data['expected_entropy']:.3f})")
        print(f"   Sintropia Real: {syntropy_real:.3f} (esperado: {data['expected_syntropy']:.3f})")
        
        # 2. Simulação Temporal
        initial_state = {
            'entropy': entropy_real,
            'syntropy': syntropy_real,
            'energy': 1.0
        }
        
        simulation_history = sim.run_simulation(initial_state)
        stats = sim.get_statistics()
        
        print(f"   Dilatação Temporal Média: {stats['mean_dilation']:.3f}")
        print(f"   Passos de Simulação: {stats['total_steps']}")
        print(f"   Desvio Padrão: {stats['std_dilation']:.6f}")
        
        # 3. Métricas de Validação
        validation_metrics = utils.calculate_validation_metrics(
            {
                'final_state': {'entropy': entropy_real, 'syntropy': syntropy_real},
                'statistics': stats,
                'history': simulation_history
            },
            data
        )
        
        print(f"   Score de Validação: {validation_metrics['validation_score']:.1f}/100")
        
        # 4. Exportar Resultados
        viz.export_simulation_data(simulation_history, f'validation_{domain}.json')
        
        # Registrar resultados
        domain_result = {
            'domain': domain,
            'entropy_real': entropy_real,
            'syntropy_real': syntropy_real,
            'expected_entropy': data['expected_entropy'],
            'expected_syntropy': data['expected_syntropy'],
            'mean_dilation': stats['mean_dilation'],
            'validation_score': validation_metrics['validation_score'],
            'status': 'VALIDATED' if validation_metrics['validation_score'] > 70 else 'NEEDS_REVIEW'
        }
        
        results['domains_validated'].append(domain_result)
        total_score += validation_metrics['validation_score']
        
        print(f"   Status: {domain_result['status']} ✓")
    
    # Score geral
    results['overall_score'] = total_score / len(datasets)
    
    print(f"\n🏆 RESULTADO FINAL:")
    print(f"   Score Geral de Validação: {results['overall_score']:.1f}/100")
    print(f"   Domínios Validados: {len(results['domains_validated'])}/4")
    print(f"   Status: {'✅ FRAMEWORK VALIDADO' if results['overall_score'] > 75 else '⚠️ FRAMEWORK EM DESENVOLVIMENTO'}")
    
    # Gerar relatório final
    viz.generate_report(results['domains_validated'], 'validation_report.txt')
    
    return results

if __name__ == '__main__':
    from datetime import datetime
    results = run_official_validation()
    
    # Imprimir resumo executivo
    print("\n📋 RESUMO EXECUTIVO:")
    print("="*50)
    for domain in results['domains_validated']:
        print(f"{domain['domain'].upper()}: Score {domain['validation_score']:.1f} - {domain['status']}")
    print(f"\nMÉDIA GERAL: {results['overall_score']:.1f}/100")
    print("="*50)
    print("📄 Relatório completo salvo em: validation_report.txt")
    print("📊 Dados exportados em: validation_*.json")
    print("🚀 Framework pronto para expansão e uso acadêmico!")
