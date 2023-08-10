import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from Datasets import ExpeDataset, SonicDataset


np.seterr(divide='ignore')

# ----------------------------------------------------------------------------
# setup
# ----------------------------------------------------------------------------

print("Processing arguments", sys.argv)

measuring_situation = sys.argv[1]
measuring_device = sys.argv[2]
durations_min = [1, 2, 3, 5, 10, 15, 30]
kernel_size = 12

match measuring_situation:
    case "ES_2023_07_08":
        expe_fn = "../data/2023_07_08/20230708-1329-Log.txt"
        sonic_fn = "../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat"
        start_date = "2023-07-08 15:00:00"
        end_date =   "2023-07-08 16:00:00"
        date = "08.07.2023"
    case "ES_2023_07_11":
        expe_fn = "../data/2023_07_11/20230711-0504-Log.txt"
        sonic_fn = "../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
        start_date = "2023-07-11 12:36:00"
        end_date =   "2023-07-11 13:36:00"
        date = "11.07.2023"
    case "GAS_2023_07_11":
        expe_fn = "../data/2023_07_11/20230711-0504-Log.txt"
        sonic_fn = "../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat"
        start_date = "2023-07-11 11:00:00"
        end_date =   "2023-07-11 12:00:00"
        date = "11.07.2023"

freqs = {"SONIC": "$\Delta t$ = 0.5 s", "EXPE": "$\Delta t$ = 1.0 s"}

# ----------------------------------------------------------------------------
# create Dataset objects
# ----------------------------------------------------------------------------

if measuring_device == "SONIC":
    ds = SonicDataset(fn=sonic_fn, start_time=start_date, end_time=end_date)
elif measuring_device == "EXPE":
    ds = ExpeDataset(fn=expe_fn, start_time=start_date, end_time=end_date)
else:
    raise ValueError("measuring_device must be 'SONIC' or 'EXPE'")

# ----------------------------------------------------------------------------
# plot
# ----------------------------------------------------------------------------

lw = 1.0 if measuring_device == "EXPE" else 0.5
raw_kw_args =           {"lw": lw, "alpha": 0.4, "c": "darkgrey"}
det_kw_args =           {"lw": lw, "alpha": 0.8, "c": "b"}
spec_kw_args =          {"lw": 0.5, "alpha": 0.5, "c": "darkgrey"}
smooth_spec_kw_args =   {"lw": 1.0, "alpha": 1.0, "c": "r"}
scat_kw_args =          {"s": 1.0, "alpha": 0.3, "c": "darkgrey"}
range_kw_args =         {"alpha": 0.1, "color": "grey"}
    

fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(20,10))
cutoff = int(kernel_size/2)

if measuring_device == "SONIC":
    
    # temperature
    ax[0,0].plot(ds.time_raw, ds.t_raw, 
               label="raw", **raw_kw_args)
    ax[0,0].plot(ds.time_raw, ds.t_det, 
               label="detrended", **det_kw_args)
    ax[1,0].plot(ds.t_freqs, ds.t_spectrum, 
               label="raw", **spec_kw_args)
    ax[1,0].scatter(ds.t_freqs, ds.t_spectrum, **scat_kw_args)
    ax[1,0].plot(ds.t_freqs[cutoff:len(ds.t_freqs)-cutoff+1], 
               ds.t_spectrum_smooth, **smooth_spec_kw_args, 
               label="smoothed")

    # 3d wind 
    ax[0,1].plot(ds.time_raw, ds.wind3d, 
               label="raw", **raw_kw_args)
    ax[0,1].plot(ds.time_raw, ds.wind3d_det, 
               label="detrended", **det_kw_args)
    ax[1,1].plot(ds.wind3d_freqs, ds.wind3d_spectrum, 
               label="raw", **spec_kw_args)
    ax[1,1].scatter(ds.wind3d_freqs, ds.wind3d_spectrum, **scat_kw_args)
    ax[1,1].plot(ds.wind3d_freqs[cutoff:len(ds.wind3d_freqs)-cutoff+1], 
               ds.wind3d_spectrum_smooth, 
               label="smoothed", **smooth_spec_kw_args)
    
    # 2d wind (horizontal wind)
    ax[0,2].plot(ds.time_raw, ds.wind2d,
                label="raw", **raw_kw_args)
    ax[0,2].plot(ds.time_raw, ds.wind2d_det,
                label="detrended", **det_kw_args)
    ax[1,2].plot(ds.wind2d_freqs, ds.wind2d_spectrum,
                label="raw", **spec_kw_args)
    ax[1,2].scatter(ds.wind2d_freqs, ds.wind2d_spectrum, **scat_kw_args)
    ax[1,2].plot(ds.wind2d_freqs[cutoff:len(ds.wind2d_freqs)-cutoff+1],
                ds.wind2d_spectrum_smooth,
                label="smoothed", **smooth_spec_kw_args)

    
    ax[0,0].set_ylabel("Temperature [°C]")
    ax[0,1].set_ylabel("3D wind speed [m/s]")
    ax[0,2].set_ylabel("2D wind speed [m/s]")
    ax[0,1].set_ylim((0, 3))
    ax[0,2].set_ylim((0, 3))

elif measuring_device == "EXPE":
    
    # temperature
    ax[0,0].plot(ds.time_raw, ds.t_raw, label="raw", **raw_kw_args)
    ax[0,0].plot(ds.time_raw, ds.t_det, label="detrended", **det_kw_args)
    ax[1,0].plot(ds.t_freqs, ds.t_spectrum, label="raw", **spec_kw_args)
    ax[1,0].scatter(ds.t_freqs, ds.t_spectrum, **scat_kw_args)
    cutoff = int(kernel_size/2)
    ax[1,0].plot(ds.t_freqs[cutoff:len(ds.t_freqs)-cutoff+1], ds.t_spectrum_smooth, 
               label="smoothed", **smooth_spec_kw_args)
    
    # relative humidity
    ax[0,1].plot(ds.time_raw, ds.rH_raw, label="raw", **raw_kw_args)
    ax[0,1].plot(ds.time_raw, ds.rH_det, label="detrended", **det_kw_args)
    ax[1,1].plot(ds.rH_freqs, ds.rH_spectrum, label="raw", **spec_kw_args)
    ax[1,1].scatter(ds.rH_freqs, ds.rH_spectrum, **scat_kw_args)
    
    ax[1,1].plot(ds.rH_freqs[cutoff:len(ds.rH_freqs)-cutoff+1], ds.rH_spectrum_smooth, 
               label="smoothed", **smooth_spec_kw_args)
    
    # pressure
    ax[0,2].plot(ds.time_raw, ds.p_raw, label="raw", **raw_kw_args)
    ax[0,2].plot(ds.time_raw, ds.p_det, label="detrended", **det_kw_args)
    ax[1,2].plot(ds.p_freqs, ds.p_spectrum, label="raw", **spec_kw_args)
    ax[1,2].scatter(ds.p_freqs, ds.p_spectrum, **scat_kw_args)
    ax[1,2].plot(ds.p_freqs[cutoff:len(ds.p_freqs)-cutoff+1], ds.p_spectrum_smooth,
                label="smoothed", **smooth_spec_kw_args)
    
    
    ax[0,0].set_ylabel("Temperature [°C]")
    ax[0,1].set_ylabel("Relative humidity [%]")
    ax[0,2].set_ylabel("Pressure [hPa]")
    
else:
    raise ValueError("measuring_device must be 'SONIC' or 'EXPE'")


for col_i in range(3):
    for row_i in range(2):
        
        # write one common text above the 2 upper plots
        title = f"Date: {date}\n\n{measuring_device} data ({freqs[measuring_device]})\n"
        fig.suptitle(title, fontweight='bold', fontsize=14)
        
        # ax[0,0].set_title(f"Date: {date}\n\n{measuring_device} data ({freqs[measuring_device]})", fontweight='bold')
        
        if row_i == 0: # time series plots
            ax[row_i, col_i].set_xlabel("Time [CET]")
            ax[row_i, col_i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
            ax[row_i, col_i].set_xlim(ds.time_raw.tolist()[0], ds.time_raw.tolist()[-1])
        
        else: # spectrum plots
            ax[row_i, col_i].axvspan(1/60, 1/600, label="1 min - 10 min", **range_kw_args)
            ax[row_i, col_i].set_ylabel("Magnitude Spectrum")
            ax[row_i, col_i].set_xlabel("Frequency [Hz]")
            ax[row_i, col_i].set_xlim(0, 0.5)
            ax[row_i, col_i].set_ylim(1e-2, 1e4)
            ax[row_i, col_i].set_yscale("log")
        
            # add secondary x axis with period in seconds below the frequency axis
            ax2 = ax[row_i, col_i].twiny()
            x_t = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
            x_t = [i*2 for i in x_t]
            # ! fix this: ax2.set_xticks(ax[row_i,col_i].get_xticks())
            ax2.set_xticks(x_t)
            ax2.set_xticklabels(np.round(1/ax[row_i, col_i].get_xticks(), 2))
            ax2.xaxis.set_ticks_position("bottom")
            ax2.xaxis.set_label_position("bottom")
            ax2.spines["bottom"].set_position(("axes", -0.25))
            ax2.set_xlabel("Period [s]")
        
        # all plots
        ax[row_i, col_i].grid(True)
        ax[row_i, col_i].legend(loc="upper right")
    
plt.tight_layout()
fn = f"{measuring_situation}_{measuring_device}_FFT.png"
plt.savefig(f"../images/results/fft/{fn}", dpi=300, bbox_inches="tight")
