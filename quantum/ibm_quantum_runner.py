# -*- coding: utf-8 -*-
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import numpy as np
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

def get_quantum_service():
    token = os.getenv('IBMQ_TOKEN')
    if not token:
        raise ValueError('Token IBM Quantum nao encontrado. Configure em .env')
    return QiskitRuntimeService(channel='ibm_quantum_platform', token=token)

def create_decoherence_circuit(t_param):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    theta = np.arccos(np.sqrt(1 - t_param))
    qc.ry(theta, 0)
    qc.measure(0, 0)
    return qc

def run_experiment(service, backend_name='least_busy', t_points=11, shots=4096):
    # ✅ Selecionar backend com menos jobs
    if backend_name == 'least_busy':
        backends = service.backends(operational=True, simulator=False)
        backend = min(backends, key=lambda b: b.status().pending_jobs)
    else:
        backend = service.backend(backend_name)
    
    print(f'Backend: {backend.name} (jobs pendentes: {backend.status().pending_jobs})')
    
    # ✅ Criar Sampler V2
    sampler = SamplerV2(mode=backend)
    
    # ✅ Criar transpiler para este backend
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=1)
    
    results = {
        'backend': backend.name,
        'timestamp': datetime.now().isoformat(),
        'shots': shots,
        'data': []
    }
    
    for i, t in enumerate(np.linspace(0, 1, t_points)):
        print(f'[{i+1}/{t_points}] t={t:.3f}')
        
        # Criar e transpilar circuito
        qc = create_decoherence_circuit(t)
        transpiled_qc = pass_manager.run(qc)
        
        # ✅ Executar com Sampler V2
        job = sampler.run([transpiled_qc], shots=shots)
        print(f'Job ID: {job.job_id()} (esperando...)')
        
        # ✅ Extrair resultados CORRETAMENTE da nova API
        result = job.result()
        
        # ✅ Formato correto da PrimitiveResult
        if hasattr(result, 'quasi_dists') and result.quasi_dists:
            dist = result.quasi_dists[0]
            # Converter para counts (probabilidades * shots)
            total_counts = shots
            counts_0 = int(dist.get(0, 0) * total_counts + 0.5)
            counts_1 = int(dist.get(1, 0) * total_counts + 0.5)
            
            # Normalizar para probabilidades
            total = counts_0 + counts_1
            if total > 0:
                p0 = counts_0 / total
                p1 = counts_1 / total
            else:
                p0 = p1 = 0.5
        else:
            # Fallback extremo
            p0 = p1 = 0.5
        
        # Calcular Model X
        if p1 > 0 and p0 > 0:
            S = - (p1 * np.log2(p1) + p0 * np.log2(p0))
        else:
            S = 0
        sigma = 1 - S
        X = sigma - S
        
        results['data'].append({
            't': t, 'p1': p1, 'entropy': S, 'syntropy': sigma, 'X': X
        })
        print(f'X = {X:.4f}, S = {S:.4f}, sigma = {sigma:.4f}')
    
    X_values = [d['X'] for d in results['data']]
    results['stats'] = {
        'average_X': np.mean(X_values),
        'std_X': np.std(X_values)
    }
    print(f"Experimento completo! Media X: {results['stats']['average_X']:.4f}")
    return results

def save_results(results, filename=None):
    os.makedirs('results', exist_ok=True)
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'results/quantum_experiment_{timestamp}.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f'Resultados salvos em: {filename}')
    return filename

if __name__ == '__main__':
    try:
        service = get_quantum_service()
        results = run_experiment(service, t_points=11, shots=4096)
        save_results(results)
    except Exception as e:
        print(f'Erro: {e}')
        import traceback
        traceback.print_exc()
