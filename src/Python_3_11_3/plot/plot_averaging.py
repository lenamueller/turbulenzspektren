import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from Datasets import ExpeDataset, SonicDataset


def diff(a: list[float], b: list[float]) -> list[float]:
    """Calculate the difference between two lists."""
    return [a[i] - b[i] for i in range(len(a))]

def plot_averaging(ds: ExpeDataset | SonicDataset, type: str) -> None:
    """Plot the averaging for different window sizes. The averaging can be done
    either by a rolling mean or by fixed intervalls."""

    durations_min = [1, 2, 3, 5, 10, 15, 30]
    durations_samples = [int(i*60/ds.sr) for i in durations_min]
    n_durations = len(durations_samples)

    # ----------------------------------------------------------------------------
    # averaging
    # ----------------------------------------------------------------------------
    
    if type == "rolling_mean":

        comparison = [ds.rolling_mean(var=ds.t_det, window_size=j) for j in durations_samples]
        assert np.shape(comparison) == (n_durations, ds.n)
        
        deviations = [diff(comparison[i], ds.t_det) for i in range(len(durations_samples))]
        assert np.shape(deviations) == (n_durations, ds.n)
        
        
    elif type == "fixed_intervalls":

        comparison = np.zeros((n_durations, ds.n))
        for i in range(n_durations):
            vals = ds.step_mean(var=ds.t_det, window_size = durations_samples[i])[:-1]
            if len(vals) < ds.n: # fill with zeros
                comparison[i] = vals + [0]*(ds.n - len(vals))
            elif len(vals) > ds.n: # cut off
                comparison[i] = vals[:ds.n]
            else:
                comparison[i] = vals
        assert np.shape(comparison) == (n_durations, ds.n)
        
        deviations = [diff(comparison[i], ds.t_det) for i in range(len(durations_samples))]
        assert np.shape(deviations) == (n_durations, ds.n)

    else:
        raise ValueError(f"Invalid averaging type '{type}'.")
    
    # ----------------------------------------------------------------------------
    # plotting
    # ----------------------------------------------------------------------------
    
    colors = plt.cm.jet(np.linspace(0,1,len(durations_samples)))
    _, ax = plt.subplots(nrows=3, ncols=1, figsize=(15,18))

    avg_kw_args =       {"lw":1.0, "alpha":0.8, "ls":'-'}
    signal_kw_args =    {"lw":0.3, "alpha":0.8, "ls":'-', "color": "darkgrey"} \
        if ds.measuring_device == "SONIC" else {"lw":1.0, "alpha":0.8, "ls":'-', "color": "darkgrey"}
    dev_kw_args =       {"lw":0.3, "alpha":0.8, "ls":'-'} \
        if ds.measuring_device == "SONIC" else {"lw":1.0, "alpha":0.8, "ls":'-'}
    
    # detrended temperature
    ax[0].plot(ds.time_raw, ds.t_det, label="EXPE (detrended)", **signal_kw_args)

    for i in range(len(durations_samples)):
        # avg line
        ax[0].plot(ds.time_raw, comparison[i], color=colors[i], **avg_kw_args,
                label=f"rolling mean {durations_min[i]} min")
        # deviation line
        ax[1].plot(ds.time_raw, deviations[i], color=colors[i],**dev_kw_args,
                label= f"{durations_min[i]} min [{np.round(np.min(deviations[i]), 2)}, {np.round(np.max(deviations[i]), 2)}]")
        # deviation box
        ax[2].boxplot(deviations[i], positions=[i], widths=0.6, patch_artist=True,
                boxprops=dict(facecolor=colors[i], color=colors[i], alpha=0.3),
                capprops=dict(color=colors[i], alpha=1),
                whiskerprops=dict(color=colors[i]), medianprops=dict(color=colors[i]),
                flierprops=dict(alpha=0.1, color=colors[i], markeredgecolor=colors[i]))

    # TODO: find a better way to set the y-limits
    # ax[1].set_ylim([-4, 4])
    # ax[2].set_ylim([-4, 4])
    
    y_labels = ["Temperature [°C]", "Temperature deviation [°C]", "Temperature deviation [°C]"]
    x_labels = ["Time [UTC]", "Time [UTC]", "Window size [min]"]
    
    for i in [0,1,2]:    
        ax[i].grid(which="minor", alpha=0.1)
        ax[i].grid(which="major", alpha=0.55)
        ax[i].set_ylabel(y_labels[i])
        ax[i].set_xlabel(x_labels[i])

    for i in [0,1]:
        ax[i].set_xlim([ds.time_raw.tolist()[0], ds.time_raw.tolist()[-1]])
        ax[i].xaxis.set_major_formatter(DateFormatter("%H:%M"))
        ax[i].legend(columnspacing=0.5, loc="upper right", fontsize="small")
    
    for i in [2]:
        ax[i].set_xticks(range(len(durations_samples)))
        ax[i].set_xticklabels(durations_min)
    
    fn = f"{ds.puo}_{ds.measuring_device}_{type}.png"
    plt.savefig(f"results/averaging/{fn}", dpi=300, bbox_inches="tight")
    plt.close()