import numpy as np, camb, emcee, matplotlib.pyplot as plt, urllib.request, os

# Get script directory and set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(os.path.dirname(script_dir), 'data')
output_dir = script_dir

# Ensure data directory exists
os.makedirs(data_dir, exist_ok=True)

# Download Planck data if not present
planck_file = os.path.join(data_dir, 'planck_tt.txt')
if not os.path.exists(planck_file):
    print("Downloading Planck CMB data...")
    urllib.request.urlretrieve(
        "https://pla.esac.esa.int/pla/aio/product-action?COSMOLOGY.FILE_ID=COM_PowerSpect_CMB-TT-full_R3.01.txt", 
        planck_file
    )
    print(f"Data saved to {planck_file}")

# Load data
ell, Dl_TT = np.loadtxt(planck_file, unpack=True, usecols=(0,1))[:2000]
def Dl_model(ell,H0,ombh2,omch2,tau,As,ns,l0):
    pars=camb.CAMBparams()
    pars.set_cosmology(H0=H0,ombh2=ombh2,omch2=omch2,tau=tau)
    pars.InitPower.set_params(As=As,ns=ns)
    Dl=camb.get_results(pars).get_cmb_power_spectra(lmax=int(ell.max()),CMB_unit="muK")["total"][:,0]
    return Dl[:len(ell)]*np.exp(-ell**2/(2*l0**2))
def lnlike(theta):
    H0,ombh2,omch2,tau,As,ns,l0=theta
    if not (50<H0<90 and 0.005<ombh2<0.025 and 0.10<omch2<0.30 and 0.04<tau<0.12 and 1e-10<As<2e-9 and 0.92<ns<1.0 and 10<l0<500): return -np.inf
    try: return -0.5*np.sum(((Dl_TT-Dl_model(ell,*theta))/(0.01*Dl_TT))**2)
    except: return -np.inf
sampler=emcee.EnsembleSampler(32,7,lnlike)
sampler.run_mcmc([np.array([67,0.022,0.12,0.06,2e-9,0.96,70])+1e-3*np.random.randn(7) for _ in range(32)],500)
l0=np.median(sampler.get_chain(discard=100,flat=True)[:,-1])
print(f"l0 = {l0:.1f}")
plt.figure(figsize=(10,6))
plt.loglog(ell,Dl_TT,"k-",label="Planck",alpha=0.7)
plt.loglog(ell,Dl_model(ell,67,0.022,0.12,0.06,2e-9,0.96,l0),"r-",label=f"Model")
plt.xlabel("Multipolo l")
plt.ylabel("DlTT (muK2)")
plt.legend()
plt.savefig(os.path.join(output_dir, "cmb.png"))
print(f"cmb.png saved to {output_dir}")