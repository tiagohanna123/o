from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit, transpile
import numpy as np
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_quantum_service():
    token = os.getenv('IBMQ_TOKEN')
    if not token:
        raise ValueError('Token IBM Quantum não encontrado. Configure em .env')
    
    return QiskitRuntimeService(
        channel='ibm_quantum',
        instance='ibm-q/open/main',
        token=token
    )

def create_decoherence_circuit(t_param):
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    theta = np.arccos(np.sqrt(1 - t_param))
    qc.ry(theta, 0)
    qc.measure(0, 0)
    return qc

def run_experiment(service, backend_name='least_busy', t_points=11, shots=4096):
    if backend_name == 'least_busy':
        backends = service.backends(
            filters=lambda b: b.configuration().n_qubits >= 2 
            and not b.configuration().simulator
        )
        from qiskit.providers.ibmq import least_busy
        backend = least_busy(backends)
    else:
        backend = service.backend(backend_name)
    
    print(f'Usando backend: {backend.name}')
    
    results = {
        'backend': backend.name,
        'timestamp': datetime.now().isoformat(),
        'shots': shots,
        'data': []
    }
    
    for i, t in enumerate(np.linspace(0, 1, t_points)):
        print(f'[{i+1}/{t_points}] t={t:.3f}')
        
        qc = create_decoherence_circuit(t)
        transpiled = transpile(qc, backend)
        
        job = backend.run(transpiled, shots=shots)
        print(f'Job ID: {job.job_id()} (esperando...)')
        
        result = job.result()
        counts = result.get_counts()
        
        p1 = counts.get('1', 0) / shots
        S = - (p1 * np.log2(p1) + (1-p1) * np.log2(1-p1)) if 0 < p1 < 1 else 0
        sigma = 1 - S
        X = sigma - S
        
        results['data'].append({
            't': t, 'p1': p1, 'entropy': S, 'syntropy': sigma, 'X': X
        })
        print(f'X = {X:.4f}, S = {S:.4f}, σ = {sigma:.4f}')
    
    X_values = [d['X'] for d in results['data']]
    results['stats'] = {
        'average_X': np.mean(X_values),
        'std_X': np.std(X_values)
    }
    
    print(f'Experimento completo! Media X: {results['stats']['average_X']:.4f}')
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
        print('\nExecute: python quantum_config.py')
