# -*- coding: utf-8 -*-
"""Motor de Simulação Avançado para Modelo X Framework"""

import numpy as np

class SimulationEngine:
    """Motor de simulação temporal com múltiplos regime"""
    
    def __init__(self, dt=0.01, max_steps=10000):
        self.dt = dt
        self.max_steps = max_steps
        self.history = []
    
    def run_simulation(self, initial_state, simulation_type="deterministic"):
        """Executa simulação temporal"""
        self.history = []
        state = initial_state.copy()  # Preservar estado original
        
        if simulation_type == "deterministic":
            return self._deterministic_simulation(state)
        else:
            return self._basic_simulation(state)
    
    def _deterministic_simulation(self, state):
        """Simulação determinística com regras fixas"""
        # Registrar estado inicial exato
        initial_dilation = state['energy'] * (1.0 + state['syntropy'] - state['entropy'])
        
        self.history.append({
            'step': 0,
            'time': 0,
            'state': state.copy(),
            'dilation': initial_dilation
        })
        
        for step in range(1, self.max_steps):
            # Calcula dilatação
            balance = state['syntropy'] - state['entropy']
            dilation = state['energy'] * (1.0 + balance)
            
            # Atualiza estado (pequenas mudanças)
            state['entropy'] += 0.001 * (balance - 0.5)
            state['syntropy'] += 0.001 * (1.0 - balance)
            state['energy'] *= 0.999
            
            # Garantir limites
            state['entropy'] = max(0.0, min(1.0, state['entropy']))
            state['syntropy'] = max(0.0, min(1.0, state['syntropy']))
            state['energy'] = max(0.1, state['energy'])
            
            self.history.append({
                'step': step,
                'time': step * self.dt,
                'state': state.copy(),
                'dilation': dilation
            })
            
            if state['energy'] < 0.1 or step >= 100:
                break
        
        return self.history
    
    def get_statistics(self):
        """Retorna estatísticas da simulação"""
        if not self.history:
            return {'total_steps': 0, 'mean_dilation': 0, 'std_dilation': 0}
        
        dilations = [h['dilation'] for h in self.history]
        return {
            'mean_dilation': sum(dilations) / len(dilations),
            'std_dilation': (sum((x - sum(dilations)/len(dilations))**2 for x in dilations) / len(dilations))**0.5,
            'total_steps': len(self.history)
        }
    
    def _basic_simulation(self, state):
        """Simulação básica quando tipo não é reconhecido"""
        return self._deterministic_simulation(state)  # Usar determinística como padrão
