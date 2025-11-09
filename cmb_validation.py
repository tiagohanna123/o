#!/usr/bin/env python3
import numpy as np, camb, emcee, matplotlib.pyplot as plt

# Baixa Planck 2018
!wget -q https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-full_R3.01.txt -O planck_tt.txt
ell, Dl_TT = np.loadtxt("planck_tt.txt", unpack=True, usecols=(0,1))[:2000]

def Dl_model(ell, H0, ombh2, omch2, tau, As, ns, l0):
    pars = camb.CAMBparams()
    pars.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, tau=tau)
    pars.InitPower.set_params(As=As, ns=ns)
    Dl = camb.get_results(pars).get_cmb_power_spectra(lmax=ell.max(), CMB_unit="muK")["total"][:,0]
    return Dl * np.exp(-ell**2/(2*l0**2))

def lnlike(theta):
    H0, ombh2, omch2, tau, As, ns, l0 = theta
    if not (50<H0<90 and 0.005<ombh2<0.1 and 1<l0<1000): return -np.inf
    return -0.5*np.sum(((Dl_TT - Dl_model(ell, *theta))/(0.01*Dl_TT))**2)

sampler = emcee.EnsembleSampler(32, 7, lnlike)
sampler.run_mcmc([np.array([67,0.022,0.12,0.06,2e-9,0.96,50]) + 1e-3*np.random.randn(7) for _ in range(32)], 2000)
l0 = np.median(sampler.get_chain(discard=500, flat=True)[:, -1])
print(f"ℓ₀ = {l0:.1f}")
plt.plot(ell, Dl_model(ell, 67,0.022,0.12,0.06,2e-9,0.96,l0)); plt.savefig("cmb.png")