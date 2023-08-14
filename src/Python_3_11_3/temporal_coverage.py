import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
import os

from Datasets import ExpeDataset, SonicDataset
from setup import metadata, create_datasets


puos = ["PUO_00_0", "PUO_00_1", "PUO_01", "PUO_02", "PUO_03", 
        "PUO_04", "PUO_05", "PUO_06", "PUO_07", "PUO_08"]

# get unique dates from metadata
dates = []
for puo in puos:
    _, _, _, _, date, day = metadata(puo)
    if date not in dates:
        dates.append(date)

# create Dataset objects
expe_datasets, sonic_datasets = create_datasets()

# get PUO ranges
ranges = []
for puo in puos[2:]: # skip first two puos without expe data
    _, _, start_date, end_date, _, day = metadata(puo)
    start = pd.to_datetime(start_date, format="%Y-%m-%d %H:%M:%S")
    end = pd.to_datetime(end_date, format="%Y-%m-%d %H:%M:%S")
    ranges.append((day-1, start, end))

# plot
fig, ax = plt.subplots(nrows=len(dates), ncols=1, figsize=(15,20))
for i in range(len(dates)):
    
    lns = [] # legend entries
    
    # PUO = period under observation
    for j in range(len(ranges)): 
        ax_i, start, end = ranges[j]
        if ax_i == i:
            hours = round((end-start).total_seconds()/(60*60), 1)
            ln_polygon = ax[i].axvspan(ranges[j][1], ranges[j][2], alpha=0.1, color='orange', label=f"PUO {j+1}: {hours} h")
            lns += [ln_polygon]
    ax[0].text(0,1.05,"PUO = Period under observation", transform=ax[0].transAxes, color="grey")

    # temperature
    lns1 = ax[i].plot(sonic_datasets[i].time_raw, sonic_datasets[i].t_det, label="SONIC Temp.", 
               lw=0.5, ls = "solid", alpha=0.5, c="darkblue")
    lns2 = ax[i].plot(expe_datasets[i].time_raw, expe_datasets[i].t_raw, label="EXPE Temp.", 
               lw=1, ls="-.", alpha=0.5, c="darkblue")
    
    # wind speed
    ax2 = ax[i].twinx()
    lns3 = ax2.plot(sonic_datasets[i].time_raw, sonic_datasets[i].wind3d,
                lw=0.2, alpha=0.5, c="r", label="SONIC wind speed")
    ax2.set_ylabel("Wind speed [m/s]", color="r")
    ax2.set_ylim((0, 10))
    
    # plot setup
    ax[i].set_title(f"{dates[i]}", fontweight='bold', color="k", fontsize=14)
    ax[i].set_ylabel("Temperature [°C]", color="darkblue")
    ax[i].set_xlabel("Time [UTC]")
    ax[i].set_ylim((10,45))
    ax[i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax[i].grid(True)

    # set common x limitation for all subplots
    date = dates[i]
    da, mo, ye = date.split(".")
    ax[i].set_xlim((
            pd.Timestamp(int(ye), int(mo), int(da), 5, 0), 
            pd.Timestamp(int(ye), int(mo), int(da), 17, 0)
            ))
    
    # legend
    lns += lns1+lns2+lns3
    labs = [l.get_label() for l in lns]
    ax[i].legend(lns, labs, loc="upper left")
    
plt.tight_layout()
plt.savefig("results/temporal_coverage.png", dpi=300, bbox_inches='tight')
