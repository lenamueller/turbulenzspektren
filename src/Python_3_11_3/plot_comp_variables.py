import matplotlib.pyplot as plt
import numpy as np

from setup import metadata, create_datasets, kernel_size
from Datasets import ExpeDataset, SonicDataset


puo = 3
expe_ds = ExpeDataset(fn="data/2023_07_11/20230711-0504-Log.txt", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00")
sonic_ds = SonicDataset(fn="data/2023_07_11/TOA5_7134.Raw_2023_07_11_0601.dat", start_time="2023-07-11 00:00:00", end_time="2023-07-11 23:59:00")

# expe_fn, sonic_fn, start_date, end_date, date, day = metadata(puo)



# x data
cutoff = int(kernel_size/2)
expe_freqs = expe_ds.t_freqs[cutoff:len(expe_ds.t_freqs)-cutoff+1]
sonic_freqs = sonic_ds.t_freqs[cutoff:len(sonic_ds.t_freqs)-cutoff+1]

# y data
expe_t_sp = expe_ds.norm_smooth_spectrum(expe_ds.t_spectrum_smooth)
expe_rH_sp = expe_ds.norm_smooth_spectrum(expe_ds.rH_spectrum_smooth)
expe_p_sp = expe_ds.norm_smooth_spectrum(expe_ds.p_spectrum_smooth)
sonic_t_sp = sonic_ds.norm_smooth_spectrum(sonic_ds.t_spectrum_smooth)
sonic_wind2d_sp = sonic_ds.norm_smooth_spectrum(sonic_ds.wind2d_spectrum_smooth)
sonic_wind3d_sp = sonic_ds.norm_smooth_spectrum(sonic_ds.wind3d_spectrum_smooth)

# diff
expe_min = np.min(np.array([expe_t_sp, expe_rH_sp, expe_p_sp]), axis=0)
expe_max = np.max(np.array([expe_t_sp, expe_rH_sp, expe_p_sp]), axis=0)
expe_diff = [i-j for i, j in zip(expe_max, expe_min)]
sonic_min = np.min(np.array([sonic_t_sp, sonic_wind2d_sp, sonic_wind3d_sp]), axis=0)
sonic_max = np.max(np.array([sonic_t_sp, sonic_wind2d_sp, sonic_wind3d_sp]), axis=0)
sonic_diff = [i-j for i, j in zip(sonic_max, sonic_min)]

# plot
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(15, 10), sharex=True)

kw_args =   {"lw": 0.5, "alpha": 0.3}

ax[0,0].plot(sonic_freqs, sonic_t_sp, label="Sonic T", **kw_args)
ax[0,0].plot(sonic_freqs, sonic_wind2d_sp, label="Sonic Wind 2D", **kw_args)
ax[0,0].plot(sonic_freqs, sonic_wind3d_sp, label="Sonic Wind 3D", **kw_args)

ax[0,1].plot(expe_freqs, expe_t_sp, label="Expe T", **kw_args)
ax[0,1].plot(expe_freqs, expe_rH_sp, label="Expe rH", **kw_args)
ax[0,1].plot(expe_freqs, expe_p_sp, label="Expe P", **kw_args)

ax[1,0].scatter(sonic_freqs, sonic_diff, s=1, color="r", alpha=0.3)
ax[1,1].scatter(expe_freqs, expe_diff, s=1, color="r", alpha=0.3)


y_limits = [(0,0.04), (0,0.08), (0,0.005), (0,0.005)]
for (row_i, col_i) in [(0,0), (0,1), (1,0), (1,1)]:
    ax[row_i, col_i].legend()
    ax[row_i, col_i].set_xlim(1e-4, 1e-1)
    ax[row_i, col_i].set_xscale("log")
    ax[row_i, col_i].set_ylim(*y_limits[row_i*2+col_i])


# bin_number = 100
# x_bins = np.logspace(-4, -1, bin_number, endpoint=True)
# y_bins = np.linspace(0, 0.005, bin_number, endpoint=True) 
# H, yedges, xedges = np.histogram2d(sonic_diff, sonic_freqs, bins=(x_bins, y_bins))
# print(xedges, yedges)
# todo
# im = ax[1,0].pcolormesh(xedges, yedges, H, cmap='rainbow')
# plt.colorbar(im, ax=ax[1,0])


fn = f"{puo}_comparison_variables.png"
plt.savefig(f"results/comparison/{fn}", dpi=300, bbox_inches="tight")
