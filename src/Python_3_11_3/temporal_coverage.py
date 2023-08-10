import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd

from Datasets import ExpeDataset, SonicDataset


# create Dataset objects

expe_datasets = [
    ExpeDataset(fn="../../data/2023_07_08/20230708-1329-Log.txt", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
    ExpeDataset(fn="../../data/2023_07_11/20230711-0504-Log.txt", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
    # TODO: update data for day 3
    ExpeDataset(fn="../../data/2023_07_11/20230711-0504-Log.txt", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00")
]
sonic_datasets = [
    SonicDataset(fn="../../data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
    SonicDataset(fn="../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
    # TODO: update data for day 3
    SonicDataset(fn="../../data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00")
]

dates = ["08.07.2023", "11.07.2023", "xx.07.2023"]

fig, ax = plt.subplots(nrows=len(dates), ncols=1, figsize=(15,12))

ranges = [
    (pd.Timestamp(2023, 7, 8, 13, 30), pd.Timestamp(2023, 7, 8, 16, 10)),
    (pd.Timestamp(2023, 7, 11, 5, 5), pd.Timestamp(2023, 7, 11, 7, 0)),
    (pd.Timestamp(2023, 7, 11, 10, 0), pd.Timestamp(2023, 7, 11, 11, 0)),
    (pd.Timestamp(2023, 7, 11, 11, 36), pd.Timestamp(2023, 7, 11, 12, 36)),
    # TODO: Add ranges for day 3
]

# create avxspan for each range in ranges
# PUO = period under observation
ax[0].axvspan(ranges[0][0], ranges[0][1], alpha=0.1, color='orange', label="PUO 1")
ax[1].axvspan(ranges[1][0], ranges[1][1], alpha=0.1, color='orange', label="PUO 2")
ax[1].axvspan(ranges[2][0], ranges[2][1], alpha=0.1, color='orange', label="PUO 3")
ax[1].axvspan(ranges[3][0], ranges[3][1], alpha=0.1, color='orange', label="PUO 4")
# TODO: add axvspan for day 3


for i in range(len(dates)):

    # temperature
    ax[i].plot(sonic_datasets[i].time_raw, sonic_datasets[i].t_det, label="SONIC Temp.", 
               lw=0.5, alpha=0.5, c="b")
    ax[i].plot(expe_datasets[i].time_raw, expe_datasets[i].t_raw, label="EXPE Temp.", 
               lw=1, alpha=0.5, c="darkblue")
    
    # wind speed
    ax2 = ax[i].twinx()
    ax2.plot(sonic_datasets[i].time_raw, sonic_datasets[i].wind3d,
                lw=0.2, alpha=0.5, c="r", label="SONIC wind speed")
    ax2.set_ylabel("Wind speed [m/s]", color="r")
    ax2.set_ylim((0, 10))
    ax2.legend(loc="upper right")

    # plot setup
    ax[i].set_title(f"{dates[i]}", fontweight='bold', fontsize=14)
    ax[i].set_ylabel("Temperature [°C]", color="b")
    ax[i].set_xlabel("Time [UTC]")
    ax[i].set_ylim((15,45))
    ax[i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    ax[i].grid(True)
    ax[i].legend(loc="upper left")
    

plt.tight_layout()
plt.savefig("../../results/temporal_coverage.png", dpi=300, bbox_inches='tight')
