import scipy.signal.windows as wf
import matplotlib.pyplot as plt
import numpy as np

from setup import KERNEL_SIZE
from Datasets import ExpeDataset, SonicDataset


functions = [
    # No parameters:
    wf.boxcar, wf.exponential, wf.blackman, wf.blackmanharris, 
    wf.bohman, wf.barthann, wf.cosine, wf.flattop, wf.hamming, wf.hann, 
    wf.lanczos, wf.nuttall, wf.parzen, wf.taylor, wf.triang, wf.tukey,
    
    # Need parameters:
    # wf.chebwin, wf.dpss, wf.gaussian, wf.general_cosine, wf.general_gaussian,
    # wf.general_hamming, wf.kaiser, wf.kaiser_bessel_derived, 
    ]

def plot_influence_windows(ds: ExpeDataset | SonicDataset) -> None:
    """Plots the influence of different window functions on the spectrum."""
    
    _, ax = plt.subplots(nrows=4, ncols=4, figsize=(14, 14),
                           sharex=True, sharey=True)
    
    for i, wf in enumerate(functions):
        
        # calculate spectrum
        ds.freqs, ds.t_spectrum = ds.calc_spectrum(
            var=ds.wind3d_det, sample_rate=ds.sr, window=wf)
        x_smooth = ds.freqs[KERNEL_SIZE//2:-KERNEL_SIZE//2+1]
        y_smooth = ds.smooth_spectrum(ds.t_spectrum)
        
        # plot spectrum
        if i == 0:
            ax[i//4, i%4].plot(x_smooth, y_smooth, label=wf.__name__, 
                               c="red", lw=0.4)
        else:
            ax[i//4, i%4].plot(x_smooth, y_smooth, label=wf.__name__, 
                               c="navy", lw=0.4)
        
        ax[i//4, i%4].set_xscale("log")
        ax[i//4, i%4].set_xlim((1e-4, 1e-1))
        ax[i//4, i%4].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax[i//4, i%4].set_title(wf.__name__)
        ax[i//4, i%4].grid(which="both", axis="both", alpha=0.2)

    plt.savefig(f"results/sensitivity_wf/wf_{ds.puo}_01.png", dpi=300, bbox_inches="tight")
    

def plot_windows() -> None:
    """Plots the influence of different window functions on the spectrum."""
    
    _, ax = plt.subplots(nrows=4, ncols=4, figsize=(14, 14),
                           sharex=True, sharey=True)
    
    for i, wf in enumerate(functions):
        
        # plot full range
        x = np.arange(100)
        y = wf(M=100)
        if i == 0:
            ax[i//4, i%4].plot(x, y, label=wf.__name__, c="red", lw=0.8)
        else:
            ax[i//4, i%4].plot(x, y, label=wf.__name__, c="grey", lw=0.8)
            
        # taper only first and last 10 %
        y = np.ones(100)
        y[:10] = wf(M=20)[:10] * y[:10]
        y[90:] = wf(M=20)[10:] * y[90:]
        if i == 0:
            ax[i//4, i%4].plot(x, y, label=wf.__name__, c="red", lw=0.8)
        else:
            ax[i//4, i%4].plot(x, y, label=wf.__name__, c="navy", lw=0.8)
        
        ax[i//4, i%4].set_title(wf.__name__)
        ax[i//4, i%4].grid(which="both", axis="both", alpha=0.2)

    plt.savefig("results/sensitivity_wf/wf.png", dpi=300, bbox_inches="tight")        