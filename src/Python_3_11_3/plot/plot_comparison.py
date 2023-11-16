import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from setup import all_puos, KERNEL_SIZE


def smooth(x: np.ndarray, y: np.ndarray, kernel_size: int) -> tuple[np.ndarray, np.ndarray]:
    """Smooths the spectrum with a moving average."""
    kernel = np.ones(kernel_size) / kernel_size
    x_smooth = x[kernel_size//2:-kernel_size//2+1]
    y_smooth = np.convolve(y, kernel, mode='valid')
    return x_smooth, y_smooth


def plot_comparison() -> None:
    """Plots the spectra of the different PUOs for the same measuring device."""
    
    # -------------------------------------------------------------------------
    # setup
    # -------------------------------------------------------------------------
    
    measuring_device = "SONIC"

    vars = {
        "SONIC": {
                    "Wind 3D":      ("freqs", "wind3d_spectrum"),
                    "Wind 2D":      ("freqs", "wind2d_spectrum"),
                    "Temp.":        ("freqs", "t_spectrum"),
                },
        "EXPE": {
                    "Temp.":        ("freqs", "t_spectrum"),
                    "rel. Feuchte": ("freqs", "rH_spectrum"),
                    "Durck":        ("freqs", "p_spectrum"),
                }
            }

    colors = {
        "Wind 3D":  "b",
        "Wind 2D":  "g",
        "Temp.":    "r"
        }

    # -------------------------------------------------------------------------
    # plotting
    # -------------------------------------------------------------------------

    _, ax = plt.subplots(3, 4, figsize=(20, 10), sharex=False, sharey=True)

    for i, puo in enumerate(all_puos):
        row_i = i // 4
        col_i = i % 4
        
        ax[row_i, col_i].set_title(puo)

        try:
            fn = f"data/spectra_data/{puo}_{measuring_device}_spectrum_data.csv"
            df = pd.read_csv(fn)
        except FileNotFoundError:
            pass

        for name, (x, y) in vars[measuring_device].items():
            x = df[x]
            y = df[y]
            
            # raw spectrum
            ax[row_i, col_i].scatter(x, y, s=0.5, alpha=0.05)
            
            # smooth spectrum
            x_smooth, y_smooth = smooth(x, y, KERNEL_SIZE)
            ax[row_i, col_i].plot(x_smooth, y_smooth, color=colors[name],
                                lw=0.3, label=f"{name}")
        
        # range
        range_kw_args = {"alpha": 0.1, "color": "orange"}
        ax[row_i, col_i].axvspan(1/(60*30), 1/(60*60), 
                                label="30 min - 60 min", **range_kw_args)
        
        # plot setup
        ax[0, 0].legend(loc='upper left')
        ax[row_i, col_i].set_xlim((1e-4, 1e-1))
        ax[row_i, col_i].set_ylim((0, 800))
        ax[row_i, col_i].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax[row_i, col_i].set_xscale("log")
        ax[row_i, col_i].set_xlabel("Frequency [Hz]")
        ax[row_i, 0].set_ylabel("Spectral density [(unit)²/Hz]")
        ax[2, 3].set_visible(False)
            
        ax2 = ax[row_i, col_i].secondary_xaxis(-0.3, functions=(lambda x: 1/x, lambda x: 1/x))
        ax2.set_xticks([10000, 1000, 100, 10])
        ax2.set_xlabel("Period [s]")
        
    plt.tight_layout()
    plt.savefig(f"results/fft/PUO_comparison_{measuring_device}.png", dpi=300, bbox_inches="tight")
    plt.close()