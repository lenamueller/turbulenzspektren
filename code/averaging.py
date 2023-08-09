import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from Datasets import ExpeDataset, SonicDataset


def diff(a: list[float], b: list[float]) -> list[float]:
    return [a[i] - b[i] for i in range(len(a))]

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

ds_expe = expe_data[0]
ds_sonic = sonic_data[0]

durations = [1, 2, 3, 5, 10, 15, 30]
colors = plt.cm.jet(np.linspace(0,1,len(durations)))
ref_temp = np.mean(ds_expe.t_det)

# variante 1: rolling mean
rolling_means = [ds_expe.rolling_mean(ds_expe.t_det, kernel_size=j*60) for j in durations]
dev_rolling = [diff(ds_expe.t_det, rolling_means[i]) for i in range(len(durations))]

# variante 2: fixed intervalls
fixed_intervalls = [ds_expe.average(ds_expe.t_det, x)[:-1] for x in durations]
dev_fixed = [diff(ds_expe.t_det, fixed_intervalls[i]) for i in range(len(durations))]


variante = 2
match variante:
    case 1:
        comparison = rolling_means
        deviations = dev_rolling
        fn = "rolling_mean.png"
    case 2:
        comparison = fixed_intervalls
        deviations = dev_fixed
        fn = "fixed_intervalls.png"
    
# ----------------------------------------------------------------------------
# plotting
# ----------------------------------------------------------------------------

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(15,18))

# detrended temperature
ax[0].plot(ds_expe.time_raw, ds_expe.t_det, lw=1, alpha=0.8, c="darkgrey", label="EXPE (detrended)")

# reference line
ax[0].axhline(y=ref_temp, c="darkgrey", lw=1.0, alpha=0.8, ls="--", 
            label=f"EXPE mean (reference)")
ax[1].axhline(y=0, c="darkgrey", lw=1.0, alpha=0.8, ls="--", 
            label=f"EXPE mean (reference)")
ax[2].axhline(y=0, c="darkgrey", lw=1.0, alpha=0.8, ls="--", 
            label=f"EXPE mean (reference)")

for i in range(len(durations)):
    # rolling mean
    ax[0].plot(ds_expe.time_raw, comparison[i], lw=1, alpha=0.8, c=colors[i], 
            label=f"rolling mean {durations[i]} min")
    # deviation line
    ax[1].plot(ds_expe.time_raw, deviations[i], lw=1.0, alpha=1.0, c=colors[i], 
        label=f"deviation {durations[i]} min [{np.round(np.min(deviations[i]), 2)}, {np.round(np.max(deviations[i]), 2)}]")
    # deviation box
    ax[2].boxplot(deviations[i], positions=[i], widths=0.6, patch_artist=True,
            boxprops=dict(facecolor=colors[i], color=colors[i], alpha=0.3),
            capprops=dict(color=colors[i], alpha=1),
            whiskerprops=dict(color=colors[i]), medianprops=dict(color=colors[i]),
            flierprops=dict(alpha=0.1, color=colors[i], markeredgecolor=colors[i]))

           
# plot setup
ax[0].set_ylim([30, 40])
ax[1].set_ylim([-4, 4])
ax[2].set_ylim([-4, 4])

ax[0].set_xlim([ds_expe.time_raw.tolist()[0], ds_expe.time_raw.tolist()[-1]])
ax[1].set_xlim([ds_expe.time_raw.tolist()[0], ds_expe.time_raw.tolist()[-1]])

ax[0].set_ylabel("Temperature [°C]")
ax[1].set_ylabel("Temperature deviation [°C]")
ax[2].set_ylabel("Temperature deviation [°C]")

ax[0].set_xlabel("Time [CET]")
ax[1].set_xlabel("Time [CET]")
ax[2].set_xlabel("Window size [min]")
ax[2].set_xticks(range(len(durations)))
ax[2].set_xticklabels(durations)

for i in [0,1]:
    ax[i].yaxis.set_major_locator(plt.MultipleLocator(1))
    ax[i].yaxis.set_minor_locator(plt.MultipleLocator(0.5))
    ax[i].xaxis.set_major_formatter(DateFormatter("%H:%M"))
    ax[i].grid(which="minor", alpha=0.1)
    ax[i].grid(which="major", alpha=0.8)
    ax[i].legend(columnspacing=0.5, loc="upper right", fontsize="small")

ax[2].yaxis.set_major_locator(plt.MultipleLocator(1))
ax[2].yaxis.set_minor_locator(plt.MultipleLocator(0.5))

ax[2].grid(axis="y", which="minor", alpha=0.1)
ax[2].grid(axis="y", which="major", alpha=0.8)


    
plt.savefig(f"images/{fn}", dpi=300, bbox_inches="tight")


