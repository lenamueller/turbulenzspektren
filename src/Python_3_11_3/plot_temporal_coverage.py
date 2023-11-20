import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd

from setup import metadata, all_puos
from setup import unique_dates as dates
from Datasets import ExpeDataset, SonicDataset


def plot_temporal_coverage() -> None:
    """Plot the temporal coverage of the experiments."""
    
    # -------------------------------------------------------------------------
    # setup
    # -------------------------------------------------------------------------
    
    expe_datasets = [ExpeDataset(puo=f"Day{i}") for i in range(1, 6)]
    sonic_datasets = [SonicDataset(puo=f"Day{i}") for i in range(1, 6)]

    ranges = []
    for puo in all_puos[:]: # skip first two puos without expe data
        _, _, start_date, end_date, _, day = metadata(puo)
        start = pd.to_datetime(start_date, format="%Y-%m-%d %H:%M:%S")
        end = pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
        ranges.append((day-1, start, end))
    
    # -------------------------------------------------------------------------
    # plotting
    # -------------------------------------------------------------------------
    
    _, ax = plt.subplots(nrows=len(dates), ncols=1, figsize=(15,20))

    for i in range(len(dates)):
        ax2 = ax[i].twinx() # secondary y-axis for wind speed
        
        lns = [] # legend entries

        lns1 = ax[i].plot(
            sonic_datasets[i].time_raw, sonic_datasets[i].t_det, label="SONIC Temp.", 
            lw=0.5, ls = "solid", alpha=0.5, c="darkblue")
        lns2 = ax[i].plot(
            expe_datasets[i].time_raw, expe_datasets[i].t_raw, label="EXPE Temp.", 
            lw=1, ls="-.", alpha=0.5, c="darkblue")
        lns3 = ax2.plot(
            sonic_datasets[i].time_raw, sonic_datasets[i].wind3d, lw=0.2, alpha=0.5, 
            c="r", label="SONIC wind speed")
        
        for j in range(len(ranges)): 
            ax_i, start, end = ranges[j]
            if ax_i == i:
                hours = round((end-start).total_seconds()/(60*60), 1)
                ln_polygon = ax[i].axvspan(ranges[j][1], ranges[j][2], alpha=0.1, 
                                            color='gold', label=f"PUO {j+1}: {hours} h")
                lns += [ln_polygon]
        
        ax[i].set_title(f"{dates[i]}", fontweight='bold', color="k", fontsize=14)
        ax[0].text(0,1.05,"PUO = Period under observation", transform=ax[0].transAxes, 
                    color="grey")
        ax[i].set_ylabel("Temperature [°C]", color="darkblue")
        ax[i].set_xlabel("Time [UTC]")
        ax2.set_ylabel("Wind speed [m/s]", color="r")
        ax[i].set_ylim((10,45))
        ax2.set_ylim((0, 10))
        ax[i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
        ax[i].grid(True)

        date = dates[i]
        da, mo, ye = date.split(".")
        ax[i].set_xlim((
                pd.Timestamp(int(ye), int(mo), int(da), 5, 0), 
                pd.Timestamp(int(ye), int(mo), int(da), 17, 0)
                ))
        
        lns += lns1+lns2+lns3
        labs = [l.get_label() for l in lns]
        ax[i].legend(lns, labs, loc="upper left")
        
    plt.tight_layout()
    plt.savefig("results/temporal_coverage/temporal_coverage.png", dpi=600, bbox_inches='tight')
    plt.close()