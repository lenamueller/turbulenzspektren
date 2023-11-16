import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

from Datasets import ExpeDataset, SonicDataset
from setup import metadata



def plot_averaging(puo: str, measuring_device: str) -> None:
    """Plot the averaging for different window sizes. The averaging can be done
    either by a rolling mean or by fixed intervalls."""

    expe_fn, sonic_fn, start_date, end_date, date, _ = metadata(puo)
    durations_min = [1, 2, 3, 5, 10, 15, 30]

    # ----------------------------------------------------------------------------
    # create Dataset objects
    # ----------------------------------------------------------------------------

    if measuring_device == "SONIC":
        ds = SonicDataset(fn=sonic_fn, start_time=start_date, end_time=end_date)
        durations = [i*60*2 for i in durations_min] # in number of samples (2 Hz)
    elif measuring_device == "EXPE":
        ds = ExpeDataset(fn=expe_fn, start_time=start_date, end_time=end_date)
        durations = [i*60 for i in durations_min] # in number of samples (1 Hz)
    else:
        raise ValueError("measuring_device must be 'SONIC' or 'EXPE'")

    # ----------------------------------------------------------------------------
    # averaging
    # ----------------------------------------------------------------------------

    n_samples = len(ds.time_raw)
    n_durations = len(durations)
    ref_temp = np.mean(ds.t_det)

    def diff(a: list[float], b: list[float]) -> list[float]:
        return [a[i] - b[i] for i in range(len(a))]

    # option 1: rolling mean
    rolling_means = [ds.rolling_mean(var=ds.t_det, window_size=j) for j in durations]
    assert np.shape(rolling_means) == (n_durations, n_samples)

    dev_rolling = [diff(rolling_means[i], ds.t_det) for i in range(len(durations))]
    assert np.shape(dev_rolling) == (n_durations, n_samples)

    # option 2: fixed intervalls
    fixed_intervalls = np.zeros((n_durations, n_samples))
    for i in range(n_durations):
        vals = ds.step_mean(var=ds.t_det, window_size = durations[i])[:-1]
        if len(vals) < n_samples:
            # fill with zeros
            fixed_intervalls[i] = vals + [0]*(n_samples - len(vals))
        elif len(vals) > n_samples:
            # cut off
            fixed_intervalls[i] = vals[:n_samples]
        else:
            fixed_intervalls[i] = vals
    assert np.shape(fixed_intervalls) == (n_durations, n_samples)

    dev_fixed = [diff(fixed_intervalls[i], ds.t_det) for i in range(len(durations))]
    assert np.shape(dev_fixed) == (n_durations, n_samples)

    # ----------------------------------------------------------------------------
    # plotting
    # ----------------------------------------------------------------------------

    colors = plt.cm.jet(np.linspace(0,1,len(durations)))

    for avg_option in ["rolling_mean", "fixed_intervalls"]:
        
        match avg_option:
            case "rolling_mean":
                comparison = rolling_means
                deviations = dev_rolling
                fn = f"{puo}_{measuring_device}_rolling_mean.png"
            case "fixed_intervalls":
                comparison = fixed_intervalls
                deviations = dev_fixed
                fn = f"{puo}_{measuring_device}_fixed_intervalls.png"
        
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(15,18))

        signal_kw_args =    {"lw":0.3, "alpha":0.8, "ls":'-', "color": "darkgrey"} if measuring_device == "SONIC" else {"lw":1.0, "alpha":0.8, "ls":'-', "color": "darkgrey"}
        axhline_kw_args =   {"lw":1.0, "alpha": 0.8, "ls":'--', "color":"darkgrey"}
        avg_kw_args =       {"lw":1.0, "alpha":0.8, "ls":'-'}
        dev_kw_args =       {"lw":0.3, "alpha":0.8, "ls":'-'} if measuring_device == "SONIC" else {"lw":1.0, "alpha":0.8, "ls":'-'}
        
        # detrended temperature
        ax[0].plot(ds.time_raw, ds.t_det, label="EXPE (detrended)", **signal_kw_args)

        # reference line
        ax[0].axhline(y=ref_temp, label="EXPE mean (reference)", **axhline_kw_args)
        ax[1].axhline(y=0, label="EXPE mean (reference)",**axhline_kw_args)
        ax[2].axhline(y=0, label="EXPE mean (reference)",**axhline_kw_args)

        for i in range(len(durations)):
            # avg line
            ax[0].plot(ds.time_raw, comparison[i], 
                    label=f"rolling mean {durations_min[i]} min", 
                    color=colors[i], **avg_kw_args)
            # deviation line
            ax[1].plot(ds.time_raw, deviations[i], 
                    label= f"deviation {durations_min[i]} min [{np.round(np.min(deviations[i]), 2)}, {np.round(np.max(deviations[i]), 2)}]",
                    color=colors[i],**dev_kw_args)
            # deviation box
            ax[2].boxplot(deviations[i], positions=[i], widths=0.6, patch_artist=True,
                    boxprops=dict(facecolor=colors[i], color=colors[i], alpha=0.3),
                    capprops=dict(color=colors[i], alpha=1),
                    whiskerprops=dict(color=colors[i]), medianprops=dict(color=colors[i]),
                    flierprops=dict(alpha=0.1, color=colors[i], markeredgecolor=colors[i]))

        # plot setup
        if avg_option == "fixed_intervalls" and np.min(fixed_intervalls) == 0.0:
            ax[0].set_ylim([28, np.max(fixed_intervalls)])
        
        for i in [1, 2]:
            ax[i].set_ylim([-4, 4])
            ax[i].set_ylabel("Temperature deviation [°C]")

        for i in [0,1]:
            ax[i].set_xlim([ds.time_raw.tolist()[0], ds.time_raw.tolist()[-1]])
            ax[i].yaxis.set_major_locator(plt.MultipleLocator(1))
            ax[i].yaxis.set_minor_locator(plt.MultipleLocator(0.5))
            ax[i].xaxis.set_major_formatter(DateFormatter("%H:%M"))
            ax[i].grid(which="minor", alpha=0.1)
            ax[i].grid(which="major", alpha=0.8)
            ax[i].legend(columnspacing=0.5, loc="upper right", fontsize="small")
            ax[i].set_xlabel("Time [UTC]")

        ax[0].set_ylabel("Temperature [°C]")
        ax[2].set_xlabel("Window size [min]")
        ax[2].set_xticks(range(len(durations)))
        ax[2].set_xticklabels(durations_min)
        ax[2].yaxis.set_major_locator(plt.MultipleLocator(1))
        ax[2].yaxis.set_minor_locator(plt.MultipleLocator(0.5))
        ax[2].grid(axis="y", which="minor", alpha=0.1)
        ax[2].grid(axis="y", which="major", alpha=0.8)
            
        plt.savefig(f"results/averaging/{fn}", dpi=300, bbox_inches="tight")
        plt.close()