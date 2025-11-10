# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'src')

from model_x import EnergyModulatedModel

print('=' * 50)
print('  Modelo X Framework v2 - Demonstração')
print('=' * 50)

# Teste rápido
model = EnergyModulatedModel(entropy=0.3, syntropy=0.7, energy=1.5)
print(f'\nDilatação temporal: {model.compute_temporal_dilation():.4f}')

print('\n' + '=' * 50)
