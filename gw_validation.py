#!/usr/bin/env python3
import numpy as np, matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries
from pycbc.waveform import get_td_waveform

!wget -q https://www.gw-openscience.org/eventapi/html/GWTC/GW150914/v3/H-H1_GWOSC_4KHZ_R1-1126259447-32.txt.gz
strain = TimeSeries.read("H-H1_GWOSC_4KHZ_R1-1126259447-32.txt.gz", format='ascii.gz').whiten(4,2).bandpass(30,400)
hp, hc = get_td_waveform(approximant='SEOBNRv4', mass1=36, mass2=29, delta_t=strain.dt.value, f_lower=30)

def snr_X(kappa):
    return (hp * np.exp(-kappa*0.1*np.exp(-np.arange(len(hp))*hp.dt/0.05))).max()

kappas = np.linspace(0,50,100)
best = kappas[np.argmax([snr_X(k) for k in kappas])]
print(f"κ = {best:.1f}")
plt.plot(kappas, [snr_X(k) for k in kappas]); plt.savefig("gw.png")