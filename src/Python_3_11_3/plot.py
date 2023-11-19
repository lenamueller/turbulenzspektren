import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from process import detrend_signal, taper_signal, calc_spectrum, smooth, roll_mean


grid_kwargs =           {"color":"lightgrey", "lw":0.4}
line_kwargs =           {"color":"mediumblue", "lw":0.6}
smooth_spec_kw_args =   {"lw": 1.0, "alpha": 0.5, "c": "r"}
title_kwargs =          {"fontweight":"bold", "fontsize":12, "color":"grey"}
scat_kw_args =          {"s": 1.0, "alpha": 0.6, "c": "darkgrey"}
range_kw_args =         {"alpha": 0.1, "color": "orange"}
    

def plot_ts(
        x: np.ndarray, y: np.ndarray,
        fn: str, title: str
        ) -> None:
    """Plots the processing steps (raw, detrend, taper) of a time series."""
    
    fig, ax = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(10,7))
    
    # plot data
    ax[0].set_title("A. Raw", loc="left")
    ax[0].plot(x, y, **line_kwargs)
    ax[1].set_title("B. Detrended", loc="left")
    ax[1].plot(x, detrend_signal(y), **line_kwargs)
    ax[2].set_title("C. Tapered", loc="left")
    ax[2].plot(x, taper_signal(detrend_signal(y), 0.1), **line_kwargs)
    
    # plot config
    fig.suptitle(title, **title_kwargs)
    ax[2].set_xlabel("Time [UTC]")
    for row_i in range(3):
        ax[row_i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax[row_i].set_xlim(x[0], x[-1])
        ax[row_i].grid(True, **grid_kwargs)
    
    plt.savefig(f"plots/preprocessing/preprocess_{fn}.png", dpi=300, bbox_inches="tight")

def plot_spectrum(
        x: np.ndarray, y: np.ndarray,
        fn: str, ylabel: str, title: str
        ) -> None:
    """Plots the spectrum of a time series."""

    y_tapered = taper_signal(detrend_signal(y), 0.1)
    freq, spec = calc_spectrum(x, y_tapered)
    
    fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,7))
    fig.suptitle(title, **title_kwargs)
    
    ax[0].plot(x, y_tapered, label="Edited time series", **line_kwargs)
    ax[1].scatter(freq, spec, label="Spectrum", **scat_kw_args)
    ax[1].plot(freq, roll_mean(spec, win_len=10), label="Rolling mean", **smooth_spec_kw_args)
    ax[1].axvspan(1/(60*30), 1/(60*60), label="30 min - 60 min", **range_kw_args)
    
    ax[0].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax[0].set_xlim(x[0], x[-1])
    ax[0].set_xlabel("Time [UTC]")
    ax[0].set_ylabel(ylabel)
    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Spectral Energy Density * Frequency")
    ax[1].set_xscale("log")
    ax[1].set_xlim((1e-4, 1e-1))
    ax[1].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
    ax2 = ax[1].secondary_xaxis(-0.2, functions=(lambda x: 1/x, lambda x: 1/x))
    ax2.set_xticks([10000, 1000, 100, 10])
    ax2.set_xlabel("Period [s]")
    
    for i in [0,1]:
        ax[i].grid(True)
        ax[i].legend(loc="upper left")
        
    plt.savefig(f"plots/spectra/spec_{fn}.png", dpi=300, bbox_inches="tight")

def plot_spectrum_comp():
    """Plots a comparison of all smoothed spectra."""
    pass

def plot_avg():
    """Plots the average of a time series."""
    pass

def plot_win():
    """Plots the nonparametric window functions."""
    pass

def plot_win_influence():
    """Plots the influence of the window function."""
    pass

def plot_temporal_coverage():
    """Plots the temporal coverage of the experiments."""
    pass