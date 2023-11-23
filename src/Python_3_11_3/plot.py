import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from parse import get_var
from process import detrend_signal, taper_signal, calc_spectrum, roll_mean, calc_turb_int
from setup import all_puos, variables, metadata, window_functions, unique_dates
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
                                  lw=0.5, c="r")
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
        plt.savefig(f"plots/spectra_comparison/spectra_temporal_comparison_{device}_{var}.png", dpi=300, bbox_inches="tight")
        plt.close()

def plot_t_spectrum_comp() -> None:
    """Plots a comparison of all smoothed spectra for both devices."""
    
    var = "t_spec"
    fig, ax = plt.subplots(3, 4, figsize=(20, 12), sharex=False, sharey=False)
    fig.suptitle("Temperature [°C]\n", **title_kwargs)

    for i, puo in enumerate(all_puos):
        
        ax[i // 4, i % 4].axvspan(1/(60*30), 1/(60*60), label="30 min - 60 min", 
                                    **range_kw_args)
        
        for device in ["EXPE", "SONIC"]:
            df = pd.read_csv(f"data/spectra_data/{puo}_{device}_spectrum_data.csv")
            if device == "EXPE":
                ax[i // 4, i % 4].plot(df["frequencies"], roll_mean(df[var], win_len=10), 
                                lw=0.5, c="b", label="EXPE (1 Hz)")
            else:
                ax[i // 4, i % 4].plot(df["frequencies"], roll_mean(df[var], win_len=10), 
                                lw=0.5, c="g", label="SONIC (2 Hz)")
            
        _, _, start_datetime, end_datetime, date, _ = metadata(puo)
        ax[i // 4, i % 4].set_title(f"{puo}:\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}", **title_kwargs)
        ax[0, 0].legend(loc='upper right')
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
    plt.savefig(f"plots/spectra_comparison/spectra_temporal_comparison_EXPE_SONIC_t.png", dpi=300, bbox_inches="tight")
    plt.close()

def plot_avg(x: np.ndarray, y: np.ndarray, device: str, title: str, fn: str) -> None:
    """Plots the average of a time series."""

    fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,7), sharex=True)
    fig.suptitle(title, **title_kwargs)
    
    colors = plt.cm.jet(np.linspace(0,1,len(WINDOWS_MIN)))
    lw = {"EXPE": 0.8, "SONIC": 0.4}
    
    # plot detrended signal
    y_det = detrend_signal(y)
    ax[0].plot(x, y_det, label="Detrended signal", color="grey", lw=lw[device])
    
    # plot rolling mean and deviation
    win_lens = [i*60*SAMPLE_RATE[device] for i in WINDOWS_MIN]
    for i, win_len in enumerate(win_lens):
        y_roll = roll_mean(y_det, win_len)
        y_dev = y_det - y_roll
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

def plot_win() -> None:
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

def plot_temporal_coverage() -> None:
    """Plots the temporal coverage of the experiments."""
    
    _, ax = plt.subplots(nrows=len(unique_dates), ncols=1, figsize=(15,20))
        
    for i in range(len(unique_dates)):
        
        # get data
        period = f"Day{i+1}"
        expe_dt = get_var("EXPE", period, "Datetime")
        expe_t = get_var("EXPE", period, "t")
        sonic_dt = get_var("SONIC", period, "Datetime")
        sonic_t = get_var("SONIC", period, "t")
        sonic_3dwind = get_var("SONIC", period, "wind3d")
                
        ax2 = ax[i].twinx() # secondary y-axis for wind speed
        
        lns = [] # legend entries

        # plot data
        lns1 = ax[i].plot(
            sonic_dt, sonic_t, label="SONIC Temp.", 
            lw=0.5, ls = "solid", alpha=0.5, c="darkblue")
        lns2 = ax[i].plot(
            expe_dt, expe_t, label="EXPE Temp.", 
            lw=1, ls="-.", alpha=0.5, c="darkblue")
        lns3 = ax2.plot(
            sonic_dt, sonic_3dwind, lw=0.2, alpha=0.5, 
            c="r", label="SONIC wind speed")
    
        # highlight puos
        ranges = []
        for puo in all_puos:
            _, _, start_date, end_date, _, day = metadata(puo)
            start = pd.to_datetime(start_date, format="%Y-%m-%d %H:%M:%S")
            end = pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
            ranges.append((day-1, start, end))
            
        for j in range(len(ranges)): 
            ax_i, start, end = ranges[j]
            if ax_i == i:
                hours = round((end-start).total_seconds()/(60*60), 1)
                ln_polygon = ax[i].axvspan(ranges[j][1], ranges[j][2], alpha=0.1, 
                                            color='gold', label=f"PUO {j+1}: {hours} h")
                lns += [ln_polygon]
        
        # plot config
        ax[i].set_title(f"{unique_dates[i]}", fontweight='bold', color="k", fontsize=14)
        ax[0].text(0,1.05,"PUO = Period under observation", transform=ax[0].transAxes, 
                    color="grey")
        ax[i].set_ylabel("Temperature [°C]", color="darkblue")
        ax[i].set_xlabel("Time [UTC]")
        ax2.set_ylabel("Wind speed [m/s]", color="r")
        ax[i].set_ylim((10,45))
        ax2.set_ylim((0, 10))
        ax[i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax[i].grid(True)

        date = unique_dates[i]
        da, mo, ye = date.split(".")
        ax[i].set_xlim((
                pd.Timestamp(int(ye), int(mo), int(da), 5, 0), 
                pd.Timestamp(int(ye), int(mo), int(da), 17, 0)
                ))
        
        lns += lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        ax[i].legend(lns, labs, loc="upper left")
        
    plt.tight_layout()
    plt.savefig("plots/temporal_coverage/temporal_coverage.png", 
                dpi=600, bbox_inches='tight')
    plt.close()

def plot_turbulent_intensity() -> None:
    """Plot a box plot of turbulence intensity for all variables."""
    
    results = {"t_expe": [], "rh": [], "p": [], "t_sonic": [], 
               "wind3d": [], "wind2d": []}

    for period in all_puos:
        results["t_expe"].append(calc_turb_int(y=get_var("EXPE", period, "t")))
        results["rh"].append(calc_turb_int(y=get_var("EXPE", period, "rh")))
        results["p"].append(calc_turb_int(y=get_var("EXPE", period, "p")))
        results["t_sonic"].append(calc_turb_int(y=get_var("SONIC", period, "t")))
        results["wind3d"].append(calc_turb_int(y=get_var("SONIC", period, "wind3d")))
        results["wind2d"].append(calc_turb_int(y=get_var("SONIC", period, "wind2d")))
        
    _, ax = plt.subplots(figsize=(10, 7))
    ax.boxplot(results.values())
    labels = ["Temperature (EXPE)", "Rel. humidity (EXPE)", "Pressure (EXPE)",
              "Temperature (SONIC)", "3D Wind (SONIC)", "2D Wind (SONIC)"]
    ax.set_xticklabels(labels)
    ax.set_ylabel("Turbulent intensity [-]")
    plt.grid()
    plt.tight_layout()
    plt.savefig("plots/other/turbulent_intensity.png", 
                dpi=600, bbox_inches='tight')
    plt.close()

def plot_patterns(period: str) -> None:
    """Plot all spectra for a single period under observation."""
    
    _, ax = plt.subplots(1, 1, figsize=(10, 7))
    
    # norm spectra
    df = pd.read_csv(f"data/spectra_data/comparison_{puo}.csv")
    df = (df-df.min())/(df.max()-df.min())
    
    # calculate mean column
    df["mean"] = df.mean(axis=1)
    df["std"] = df.std(axis=1)
    
    # del first row for better plotting
    df = df.iloc[1:, :]
    
    # reduce spectra to first 300 rows
    first_n = 300
    df = df.iloc[:first_n, :]
    
    # plot spectra
    x = df["frequencies"]
    plt.plot(x, roll_mean(df["EXPE_t"], win_len=10), label="EXPE: T", 
             lw=1.0, ls="solid", c="red", alpha=0.7)
    plt.plot(x, roll_mean(df["EXPE_rh"], win_len=10), label="EXPE: rH", 
             lw=1.0, ls="solid", c="c", alpha=0.7)
    plt.plot(x, roll_mean(df["EXPE_p"], win_len=10), label="EXPE: p", 
             lw=1.0, ls="solid", c="b", alpha=0.7)
    plt.plot(x, roll_mean(df["SONIC_t"], win_len=10), label="SONIC: T", 
             lw=1.0, ls="--", c="r", alpha=0.7)
    plt.plot(x, roll_mean(df["SONIC_wind2d"], win_len=10), label="SONIC: 2D wind", 
             lw=1.0, ls="--", c="limegreen", alpha=0.7)
    plt.plot(x, roll_mean(df["SONIC_wind3d"], win_len=10), label="SONIC: 3D wind", 
             lw=1.0, ls="--", c="darkgreen", alpha=0.7)
    
    # plot mean and confidence interval
    plt.plot(x, roll_mean(df["mean"], win_len=10), label="Mean",
                lw=1.0, ls="solid", c="k")
    plt.fill_between(x, roll_mean(df["mean"]-0.5*df["std"], win_len=10),
                        roll_mean(df["mean"]+0.5*df["std"], win_len=10),
                        color="grey", alpha=0.3, label="Confidence interval (0.5*Std)")
    
    # 30 to 60 min range
    plt.axvspan(1/(60*30), 1/(60*60), label="30 min - 60 min", **range_kw_args)
    
    # plot setup
    _, _, start_datetime, end_datetime, date, _ = metadata(period)
    plt.title(f"{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}", **title_kwargs)
    plt.ylim(bottom=-0.1)
    plt.ylabel("Normalized spectral Energy Density * Frequency")
    plt.xlabel("Frequency [Hz]")
    plt.xscale("log")
    plt.xlim((1e-4, 1e-1))
    plt.xticks([1e-4, 1e-3, 1e-2, 1e-1])
    plt.legend()
    plt.grid()
    ax2 = ax.secondary_xaxis(-0.15, functions=(lambda x: 1/x, lambda x: 1/x))
    ax2.set_xticks([10000, 1000, 100, 10])
    ax2.set_xlabel("Period [s]")
    plt.savefig(f"plots/spectra_comparison/spectra_variable_comparison_{period}.png", bbox_inches="tight", dpi=300)
    plt.close()
    
def plot_corr():
    
    corr_dfs = []
    
    for period in all_puos:
        df = pd.read_csv(f"data/spectra_data/comparison_{period}.csv")
        
        # reduce spectra to first 300 rows
        first_n = 300
        df = df.iloc[:first_n, :]

        # apply roll_mean to each column
        df = df.apply(roll_mean, win_len=10)

        rename_dict = {
            "EXPE_t": "EXPE: T",
            "EXPE_rh": "EXPE: rH",
            "EXPE_p": "EXPE: p",
            "SONIC_t": "SONIC: T",
            "SONIC_wind2d": "SONIC: 2D wind",
            "SONIC_wind3d": "SONIC: 3D wind"
            }
        df = df.rename(columns=rename_dict)
        df = df.iloc[:, 1:]
        
        # min max normalize
        df = (df-df.min())/(df.max()-df.min())

        # Computes feature correlation
        corr_dfs.append(df.corr(method="pearson"))
        
        # calculate mean of allv alues in df
        print(period, round(df.mean().mean(), 2))
    
    # calculate mean correlation 
    df_corr = pd.concat(corr_dfs).groupby(level=0).mean()
    df_corr = df_corr.reindex(index=df_corr.columns)
    
    labels = np.where(np.abs(df_corr)>0.75, "Strong",
                  np.where(np.abs(df_corr)>0.5, "Medium",
                           np.where(np.abs(df_corr)>0.25, "Weak", "")))
    
    # Plot correlation matrix
    plt.figure(figsize=(15, 13))
    sns.heatmap(df_corr, 
                mask=np.eye(len(df_corr)), 
                center=0, 
                annot=True, fmt=".2f",
                # annot=labels, fmt="",
                linewidths=.5,
                cmap="vlag", vmin=-1, vmax=1,
                cbar_kws={"shrink": 0.8}
                )
    
    plt.savefig(f"plots/other/correlation_mean.png", bbox_inches="tight", dpi=300)
    plt.close()
