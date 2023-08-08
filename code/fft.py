import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from Datasets import ExpeDataset, SonicDataset


# ----------------------------------------------------------------------------
# setup
# ----------------------------------------------------------------------------

plot_fn = "FFT_ES_ES" # FFT_GAS_ES, FFT_ES_ES

# data paths and temporal frame of measurements
match plot_fn:

    case "FFT_ES_ES":
        expe_fns = ["data/2023_07_08/20230708-1329-Log.txt", "data/2023_07_11/20230711-0504-Log.txt"]
        sonic_fns = ["data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat", "data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"]
        
        d1_start_date = "2023-07-08 15:00:00" # ES d1
        d1_end_date =   "2023-07-08 16:00:00" # ES d1
        d2_start_date = "2023-07-11 12:36:00" # ES d2
        d2_end_date =   "2023-07-11 13:36:00" # ES d2
        
    case "FFT_GAS_ES":
        expe_fns = ["data/2023_07_11/20230711-0504-Log.txt", "data/2023_07_11/20230711-0504-Log.txt"]
        sonic_fns = ["data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", "data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"]
        
        d1_start_date = "2023-07-11 11:00:00" # GAS d2
        d1_end_date =   "2023-07-11 12:00:00" # GAS d2
        d2_start_date = "2023-07-11 12:36:00" # ES d2
        d2_end_date =   "2023-07-11 13:36:00" # ES d2

# ----------------------------------------------------------------------------
# create Dataset objects
# ----------------------------------------------------------------------------

expe_data = [
    ExpeDataset(fn=expe_fns[0], start_time=d1_start_date, end_time=d1_end_date),
    ExpeDataset(fn=expe_fns[1], start_time=d2_start_date, end_time=d2_end_date)
]
sonic_data = [
    SonicDataset(fn=sonic_fns[0], start_time=d1_start_date, end_time=d1_end_date),
    SonicDataset(fn=sonic_fns[1], start_time=d2_start_date, end_time=d2_end_date)
]

# ----------------------------------------------------------------------------
# plot
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(nrows=6, ncols=2, figsize=(18,20))

for col_i in [0,1]:

    # keywords arguments
    raw_kw_args =           {"lw": 1.0, "alpha": 0.4, "c": "darkgrey", "label": "raw"}
    det_kw_args =           {"lw": 1.0, "alpha": 0.8, "c": "b", "label": "detrended"}
    spec_kw_args =          {"lw": 0.5, "alpha": 0.5, "c": "darkgrey", "label": "raw spectrum"}
    smooth_spec_kw_args =   {"lw": 1.0, "alpha": 1.0, "c": "r", "label": "smooth spectrum"}
    scat_kw_args =          {"s": 1.0, "alpha": 0.3, "c": "darkgrey"}

    # EXPE time series
    ax[0,col_i].plot(expe_data[col_i].time_raw, expe_data[col_i].t_raw, **raw_kw_args)
    ax[0,col_i].plot(expe_data[col_i].time_raw, expe_data[col_i].t_det, **det_kw_args)
    
    # EXPE temperature spectrum
    ax[1,col_i].plot(expe_data[col_i].freqs_t, expe_data[col_i].spectrum_t, **spec_kw_args)
    ax[1,col_i].scatter(expe_data[col_i].freqs_t, expe_data[col_i].spectrum_t, **scat_kw_args)
    cutoff = int(expe_data[col_i].kernel_size/2)
    ax[1, col_i].plot(expe_data[col_i].freqs_t[cutoff:len(expe_data[col_i].freqs_t)-cutoff+1], 
                      expe_data[col_i].t_spectrum_smooth, **smooth_spec_kw_args)
    
    # SONIC temperature time series
    ax[2,col_i].plot(sonic_data[col_i].time_raw, sonic_data[col_i].t_raw, **raw_kw_args)
    ax[2,col_i].plot(sonic_data[col_i].time_raw, sonic_data[col_i].t_raw, **det_kw_args)
    
    # SONIC temperature spectrum
    ax[3,col_i].plot(sonic_data[col_i].t_freq, sonic_data[col_i].t_spectrum, **spec_kw_args)
    ax[3,col_i].scatter(sonic_data[col_i].t_freq, sonic_data[col_i].t_spectrum, **scat_kw_args)
    cutoff = int(sonic_data[col_i].kernel_size/2)
    ax[3, col_i].plot(sonic_data[col_i].t_freq[cutoff:len(sonic_data[col_i].t_freq)-cutoff+1], 
                      sonic_data[col_i].t_spectrum_smooth, **smooth_spec_kw_args)

    # SONIC wind speed time series
    ax[4,col_i].plot(sonic_data[col_i].time_raw, sonic_data[col_i].wind_total, **raw_kw_args)
    ax[4,col_i].plot(sonic_data[col_i].time_raw, sonic_data[col_i].wind_total_det, **det_kw_args)
    
    # SONIC wind speed spectrum
    ax[5,col_i].plot(sonic_data[col_i].wind_freq, sonic_data[col_i].wind_spectrum, **spec_kw_args)
    ax[5,col_i].scatter(sonic_data[col_i].wind_freq, sonic_data[col_i].wind_spectrum, **scat_kw_args)
    cutoff = int(sonic_data[col_i].kernel_size/2)
    ax[5, col_i].plot(sonic_data[col_i].wind_freq[cutoff:len(sonic_data[col_i].wind_freq)-cutoff+1], 
                      sonic_data[col_i].wind_spectrum_smooth, **smooth_spec_kw_args)
    
    # range from 1 min to 10 min
    for row_i in [1, 3, 5]:
        ax[row_i, col_i].axvspan(1/60, 1/600, alpha=0.1, color="grey", label="1 min - 10 min")
    
    # plot setup
    ax[0,col_i].set_title(f"Date: {expe_data[col_i].date}\n\nEXPE data ($\Delta t$ = 1 s)", 
                          fontweight='bold')
    ax[2, col_i].set_title("SONIC data ($\Delta t$ = 0.5 s)", fontweight='bold')
    
    ax[0,col_i].set_ylabel("Temperature [°C]")
    ax[2,col_i].set_ylabel("Temperature [°C]")
    ax[4, col_i].set_ylabel("Wind speed [m/s]")
    
    ax[0,col_i].set_xlabel(f"Time [CET]")
    ax[2,col_i].set_xlabel(f"Time [CET]")
    ax[4,col_i].set_xlabel(f"Time [CET]")
        
    for row_i in [0, 2, 4]:
        ax[row_i, col_i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax[row_i, col_i].set_xlim(
            expe_data[col_i].time_raw.tolist()[0],
            expe_data[col_i].time_raw.tolist()[-1])
        
    for row_i in [1, 3, 5]:
        ax[row_i,col_i].set_xlabel("Frequency [Hz]")
        ax[row_i,col_i].set_ylabel("Magnitude Spectrum")
        ax[row_i,col_i].set_xlim(0, 0.5)
        ax[row_i, col_i].set_yscale("log")
        # ax[row_i, col_i].set_xscale("log")

        # add secondary x axis with period in seconds below the frequency axis
        ax2 = ax[row_i,col_i].twiny()
        x_t = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
        x_t = [i*2 for i in x_t]
        # ! fix this: ax2.set_xticks(ax[row_i,col_i].get_xticks())
        ax2.set_xticks(x_t)
        ax2.set_xticklabels(np.round(1/ax[row_i,col_i].get_xticks(), 2))
        ax2.xaxis.set_ticks_position("bottom")
        ax2.xaxis.set_label_position("bottom")
        ax2.spines["bottom"].set_position(("axes", -0.25))
        ax2.set_xlabel("Period [s]")
    
    temp_lims = (20, 45)
    wind_lims = (0, 3)
    mag_lims = (1e-2, 1e4)
    y_limits = [temp_lims, mag_lims, temp_lims, mag_lims, wind_lims, mag_lims]
    for row_i in [0, 1, 2, 3, 4, 5]:
        ax[row_i, col_i].grid(True)
        ax[row_i, col_i].legend(loc="upper right")
        ax[row_i, col_i].set_ylim(y_limits[row_i])
    
plt.tight_layout()
plt.savefig(f"images/{plot_fn}.png", dpi=300, bbox_inches="tight")
