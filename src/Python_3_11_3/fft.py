import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import NonUniformImage
from matplotlib.dates import DateFormatter
import matplotlib.colors as colors

from Datasets import ExpeDataset, SonicDataset
from setup import metadata, kernel_size

np.seterr(divide='ignore')

# ----------------------------------------------------------------------------
# setup
# ----------------------------------------------------------------------------

print("Processing arguments", sys.argv)

puo = sys.argv[1]
measuring_device = sys.argv[2]

expe_fn, sonic_fn, start_date, end_date, date, _ = metadata(puo)

durations_min = [1, 2, 3, 5, 10, 15, 30]

freqs = {"SONIC": "sample rate = 2 Hz, $\Delta t$ = 0.5 s", "EXPE": "sample rate = 1 Hz, $\Delta t$ = 1.0 s"}

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
spec_kw_args =          {"lw": 0.3, "alpha": 0.3, "c": "darkgrey"}
smooth_spec_kw_args =   {"lw": 1.0, "alpha": 0.5, "c": "r"}
scat_kw_args =          {"s": 1.0, "alpha": 0.6, "c": "darkgrey"}
range_kw_args =         {"alpha": 0.1, "color": "orange"}
    
def two_dim_binning(x: np.ndarray, y: np.ndarray, bins: list[tuple[float]]) -> list[list[float]]:
    assert len(x) == len(y)
    
    binned_data: list[list[float]] = [[] for i in range(len(bins))]
    for i in range(len(x)):
        x_i = x[i]
        y_i = y[i]
        for j in range(len(bins)):
            (lower, upper) = bins[j]
            if lower <= x_i < upper:
                binned_data[j].append(y_i)
    return binned_data

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
    ax[0,1].set_ylim((0, 5))
    ax[0,2].set_ylim((0, 5))

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
        
        if row_i == 0: # time series plots
            ax[row_i, col_i].set_xlabel("Time [UTC]")
            ax[row_i, col_i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
            ax[row_i, col_i].set_xlim(ds.time_raw.tolist()[0], ds.time_raw.tolist()[-1])
        
        else: # spectrum plots
            ax[row_i, col_i].axvspan(1/(60*1), 1/(60*15), label="1 min - 15 min", **range_kw_args)
            ax[row_i, col_i].set_ylabel("Spectral Energy Density * Frequency")
            ax[row_i, col_i].set_xlabel("Frequency [Hz]")
            max_smooth_val = np.max(ds.t_spectrum_smooth)
            max_smooth_val *= 1.25
            if measuring_device == "SONIC":
                ax[row_i, col_i].set_ylim((0, max_smooth_val))
            else:
                pass
            
            ax[row_i, col_i].set_xscale("log")
            ax[row_i, col_i].set_xlim((1e-4, 1e-1))
            ax[row_i, col_i].set_xticks([1e-4, 1e-3, 1e-2, 1e-1])
            
            # secondary x axis with period in seconds
            ax2 = ax[row_i, col_i].secondary_xaxis(-0.2, functions=(lambda x: 1/x, lambda x: 1/x))
            ax2.set_xticks([10000, 1000, 100, 10])
            ax2.set_xlabel("Period [s]")
            
        # all plots
        ax[row_i, col_i].grid(True)
        ax[row_i, col_i].legend(loc="upper right")
    
plt.tight_layout()
fn = f"{puo}_{measuring_device}_FFT.png"
plt.savefig(f"../../results/fft/{fn}", dpi=300, bbox_inches="tight")
