import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd

from Datasets import ExpeDataset, SonicDataset


# create Dataset objects
expe_datasets = [
    ExpeDataset(fn="data/2023_07_08/20230708-1329-Log.txt", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
    ExpeDataset(fn="data/2023_07_11/20230711-0504-Log.txt", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
    ExpeDataset(fn="data/2023_08_11/20230811-0810-Log.txt", start_time="2023-08-11 00:00:00", end_time="2023-08-11 23:59:00"),
    ExpeDataset(fn="data/2023_08_12/20230812-0641-Log.txt", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
    # todo
    ExpeDataset(fn="data/2023_08_12/20230812-0641-Log.txt", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
]
sonic_datasets = [
    SonicDataset(fn="data/2023_07_08/TOA5_7134.Raw_2023_07_08_0923.dat", start_time="2023-07-08 00:00:00", end_time="2023-07-08 23:59:00"),
    SonicDataset(fn="data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00"),
    SonicDataset(fn="data/2023_08_11/TOA5_7134.Raw_2023_08_11_0924.dat", start_time="2023-08-11 00:00:00", end_time="2023-08-11 23:59:00"),
    SonicDataset(fn="data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
    # todo
    SonicDataset(fn="data/2023_08_12/TOA5_7134.Raw_2023_08_12_0755.dat", start_time="2023-08-12 00:00:00", end_time="2023-08-12 23:59:00"),
]

dates = ["08.07.2023", "11.07.2023", "11.08.2023", "12.08.2023", "14.08.2023"]

ranges = [
    (0, pd.Timestamp(2023, 7, 8, 13, 30), pd.Timestamp(2023, 7, 8, 16, 10)),
    (1, pd.Timestamp(2023, 7, 11, 5, 5), pd.Timestamp(2023, 7, 11, 7, 0)),
    (1, pd.Timestamp(2023, 7, 11, 10, 0), pd.Timestamp(2023, 7, 11, 11, 0)),
    (1, pd.Timestamp(2023, 7, 11, 11, 36), pd.Timestamp(2023, 7, 11, 12, 36)),
    (2, pd.Timestamp(2023, 8, 11, 8, 25), pd.Timestamp(2023, 8, 11, 9, 55)),
    (2, pd.Timestamp(2023, 8, 11, 12, 20), pd.Timestamp(2023, 8, 11, 16, 50)),
    (3, pd.Timestamp(2023, 8, 12, 6, 55), pd.Timestamp(2023, 8, 12, 14, 20)),
    # todo
    (4, pd.Timestamp(2023, 8, 12, 6, 55), pd.Timestamp(2023, 8, 12, 14, 20))
]

fig, ax = plt.subplots(nrows=len(dates), ncols=1, figsize=(15,20))
for i in range(len(dates)):
    
    # legend entries
    lns = []
    
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
