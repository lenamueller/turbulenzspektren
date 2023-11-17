import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from process import detrend_signal, taper_signal


grid_kwargs = {"color":"lightgrey", "lw":0.4}
line_kwargs = {"color":"mediumblue", "lw":0.6}
title_kwargs = {"fontweight":"bold", "fontsize":12, "color":"grey"}

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

def plot_spectrum():
    """Plots the spectrum of a time series."""
    pass

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