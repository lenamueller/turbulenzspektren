import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from process import detrend_signal, taper_signal, calc_spectrum, roll_mean, sample_freq
from setup import all_puos, variables, metadata, window_functions
from setup import WINDOWS_MIN, SAMPLE_RATE


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
    plt.close()
    
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
    plt.close()
    
def plot_spectrum_comp(device: str) -> None:
    """Plots a comparison of all smoothed spectra."""
    
    labels = {
        "t_spec": "Temperature [°C]",
        "rh_spec": "Relative Humidity [%]",
        "p_spec": "Pressure [hPa]",
        "wind3d_spec": "Wind 3D [m/s]",
        "wind2d_spec": "Wind 2D [m/s]"
        }
    
    for var in variables[device]:
        var = var+"_spec"
        fig, ax = plt.subplots(3, 4, figsize=(20, 12), sharex=False, sharey=False)
        fig.suptitle(labels[var]+f"\n\n({device}, {SAMPLE_RATE[device]} Hz)", **title_kwargs)
    
        for i, puo in enumerate(all_puos):
            df = pd.read_csv(f"data/spectra_data/{puo}_{device}_spectrum_data.csv")
            
            # plot data            
            ax[i // 4, i % 4].scatter(df["frequencies"], df[var], s=0.5, alpha=0.5, 
                                     color="grey")
            ax[i // 4, i % 4].plot(df["frequencies"], roll_mean(df[var], win_len=10), 
                                  lw=0.3, c="r")
            ax[i // 4, i % 4].axvspan(1/(60*30), 1/(60*60), label="30 min - 60 min", 
                                     **range_kw_args)
            
            # plot setup
            _, _, start_datetime, end_datetime, date, _ = metadata(puo)
            ax[i // 4, i % 4].set_title(f"{puo}:\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}", **title_kwargs)
            ax[0, 0].legend(loc='upper left')
            ax[i // 4, i % 4].set_xlim((1e-4, 1e-1))
            ax[i // 4, i % 4].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
            ax[i // 4, i % 4].set_xscale("log")
            ax[i // 4, i % 4].set_xlabel("Frequency [Hz]")
            ax[i // 4, 0].set_ylabel("Spectral density [(unit)²/Hz]")
            ax[2, 3].set_visible(False)
            ax[i // 4, i % 4].grid()
                
            ax2 = ax[i // 4, i % 4].secondary_xaxis(-0.3, functions=(lambda x: 1/x, lambda x: 1/x))
            ax2.set_xticks([10000, 1000, 100, 10])
            ax2.set_xlabel("Period [s]")
            
            
        plt.tight_layout()
        plt.savefig(f"plots/spectra/spectra_comparison_{device}_{var}.png", dpi=300, bbox_inches="tight")
        plt.close()
        
def plot_avg(x: np.ndarray, y: np.ndarray, device: str, title: str, fn: str):
    """Plots the average of a time series."""

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,7), sharex=True)
    fig.suptitle(title, **title_kwargs)
    
    colors = plt.cm.jet(np.linspace(0,1,len(WINDOWS_MIN)))
    lw = {"EXPE": 0.8, "SONIC": 0.4}
    
    # plot detrended signal
    ax[0].plot(x, detrend_signal(y), label="Detrended signal", color="grey", lw=lw[device])
    
    # plot rolling mean and deviation
    win_lens = [i*60*SAMPLE_RATE[device] for i in WINDOWS_MIN]
    for i, win_len in enumerate(win_lens):
        y_roll = roll_mean(detrend_signal(y), win_len)
        y_dev = y - y_roll
        ax[1].plot(x, y_roll, label=f"Mean {WINDOWS_MIN[i]} min", color=colors[i], lw=lw[device])
        ax[2].plot(x, y_dev, label=f"Turbulence {WINDOWS_MIN[i]} min", color=colors[i], lw=lw[device])
    
    for i in range(len(ax)):
        # plot legend on right side of subplots
        ax[i].legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax[i].grid(True)
        ax[i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
        
    plt.tight_layout()
    
    plt.savefig(f"plots/averaging/{fn}.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_win():
    """Plots the nonparametric window functions."""
    
    _, ax = plt.subplots(nrows=4, ncols=4, figsize=(14, 14),
                           sharex=True, sharey=True)
    
    for i, wf in enumerate(window_functions):
        
        # plot full range
        ax[i//4, i%4].plot(
            np.arange(100), 
            taper_signal(y=np.ones(100), perc=0.5, func=wf),
            c="grey", lw=0.8, label="Full range")
        
        # taper only first and last 10 %
        ax[i//4, i%4].plot(
            np.arange(100), 
            taper_signal(y=np.ones(100), perc=0.1, func=wf),
            c="navy", lw=0.8, label="First and last 10 %")
        
        ax[i//4, i%4].set_title(wf.__name__)
        ax[i//4, i%4].grid(which="both", axis="both", alpha=0.2)

    ax[0, 0].legend(loc='center')
    plt.savefig("plots/sensitivity_wf/window_functions.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_win_influence(x: np.ndarray, y: np.ndarray, title: str, fn: str) -> None:
    """Plots the influence of different window functions on the spectrum."""
    
    fig, ax = plt.subplots(nrows=4, ncols=4, figsize=(14, 14),
                           sharex=True, sharey=True)
    
    fig.suptitle(title, **title_kwargs)
    
    for i, wf in enumerate(window_functions):
        freq, spec = calc_spectrum(x, taper_signal(detrend_signal(y), 0.1, func=wf))
        spec_roll = roll_mean(spec, win_len=10)
        
        ax[i//4, i%4].plot(freq, spec_roll, 
                           label=wf.__name__, c="navy", lw=0.4)
        ax[i//4, i%4].set_xscale("log")
        ax[i//4, i%4].set_xlim((1e-4, 1e-1))
        ax[i//4, i%4].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax[i//4, i%4].set_title(wf.__name__)
        ax[i//4, i%4].grid(which="both", axis="both", alpha=0.2)

    plt.savefig(f"plots/sensitivity_wf/{fn}.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_temporal_coverage():
    """Plots the temporal coverage of the experiments."""
    pass