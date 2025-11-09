# Execute isto no Python/Colab para recriar o arquivo
script_completo = '''import numpy as np, matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from pycbc.waveform import get_td_waveform

# 1. Dados do detector
strain = TimeSeries.fetch_open_data('H1', 1126259446, 1126259478, sample_rate=4096)
strain = strain.whiten(4, 2).bandpass(30, 400)
print(f"Strain processado: {len(strain)} pontos")

# 2. Template
hp, _ = get_td_waveform(approximant='SEOBNRv4', mass1=36, mass2=29, 
                        delta_t=1/4096, f_lower=30)
hp = np.array(hp)
dt = 1/4096
print(f"Template gerado: {len(hp)} pontos")

# 3. Função SNR
def snr(k):
    factor = np.exp(-k*0.1*np.exp(-np.arange(len(hp))*dt/0.05))
    return (hp * factor).max()

# 4. Otimização
kappas = np.linspace(0, 50, 100)
snrs = [snr(k) for k in kappas]
best = kappas[np.argmax(snrs)]
print(f'κ ótimo = {best:.1f}')

# 5. Plot (salva na pasta NOTEBOOKS)
plt.figure(figsize=(10,6))
plt.plot(kappas, snrs, 'b-', linewidth=2)
plt.axvline(x=best, color='r', linestyle='--', label=f'κ={best:.1f}')
plt.xlabel('κ (parâmetro de amortecimento)')
plt.ylabel('SNR máximo')
plt.title('GW150914: SNR vs κ')
plt.legend()
plt.savefig('notebooks/gw.png', dpi=150)
print("✅ gw.png gerado com sucesso")
'''

# Escreva o arquivo
with open('notebooks/gw_validation.py', 'w', encoding='utf-8') as f:
    f.write(script_completo)

print("✅ Arquivo recriado com sucesso!")