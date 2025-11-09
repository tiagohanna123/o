import numpy as np, camb, emcee, matplotlib.pyplot as plt, urllib.request, os

# Download Planck data
os.chdir(r'D:\Downloads\o\empirico')
urllib.request.urlretrieve('https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-full_R3.01.txt', 'planck_tt.txt')
ell, Dl_TT = np.loadtxt('planck_tt.txt', unpack=True, usecols=(0,1))

# Use apenas até ℓ=2000 para evitar ruído e garantir consistência
mask = ell <= 2000
ell = ell[mask]
Dl_TT = Dl_TT[mask]

def Dl_model(ell, H0, ombh2, omch2, tau, As, ns, l0):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, tau=tau)
    pars.InitPower.set_params(As=As, ns=ns)
    
    # Calcule até o ℓ máximo necessário
    lmax = int(ell.max())
    Dl_full = camb.get_results(pars).get_cmb_power_spectra(lmax=lmax, CMB_unit='muK')['total'][:,0]
    
    # Truncate para o tamanho de ell
    return Dl_full[:len(ell)] * np.exp(-ell**2/(2*l0**2))

def lnlike(theta):
    H0, ombh2, omch2, tau, As, ns, l0 = theta
    if not (50 < H0 < 90 and 0.005 < ombh2 < 0.025 and 0.10 < omch2 < 0.30 and 
            0.04 < tau < 0.12 and 1e-10 < As < 2e-9 and 0.92 < ns < 1.0 and 10 < l0 < 500):
        return -np.inf
    try:
        Dl = Dl_model(ell, *theta)
        return -0.5 * np.sum(((Dl_TT - Dl) / (0.01 * Dl_TT))**2)
    except:
        return -np.inf

# MCMC (500 passos para teste rápido)
sampler = emcee.EnsembleSampler(32, 7, lnlike)
initial = [np.array([67,0.022,0.12,0.06,2e-9,0.96,70]) + 1e-3*np.random.randn(7) for _ in range(32)]
sampler.run_mcmc(initial, 500)

# Resultados
samples = sampler.get_chain(discard=100, flat=True)
l0 = np.median(samples[:,-1])
print(f'ℓ₀ = {l0:.1f}')

# Plot
plt.figure(figsize=(10,6))
plt.loglog(ell, Dl_TT, 'k-', label='Planck', alpha=0.7)
plt.loglog(ell, Dl_model(ell, 67, 0.022, 0.12, 0.06, 2e-9, 0.96, l0), 'r-', label=f'Modelo ℓ₀={l0:.1f}')
plt.xlabel('Multipolo ℓ')
plt.ylabel('Dℓ^TT (μK²)')
plt.legend()
plt.savefig('cmb.png')
print("✅ cmb.png gerado")