import sys
from math import floor
import numpy as np
import pandas as pd
from scipy import fft
from scipy.signal import detrend
from sklearn.linear_model import LinearRegression
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

class ExpeDataset:
    def __init__(
            self, fn: str, 
            start_time: str,
            end_time: str):

        """Constructor"""

        self.date: str = fn[-21:-13]
        self.start_time: str = start_time
        self.end_time: str = end_time

        self.time_raw: np.ndarray = None

        self.t_raw: np.ndarray = None
        self.rF_raw: np.ndarray = None
        self.p_raw: np.ndarray = None

        self.t_det: np.ndarray = None
        self.rF_det: np.ndarray = None
        self.p_det: np.ndarray = None

        
        self.nf: int = None
        
        self.t_freqs: np.ndarray = None
        self.rF_freqs: np.ndarray = None
        self.p_freqs: np.ndarray = None

        self.t_spectrum: np.ndarray = None
        self.rF_spectrum: np.ndarray = None
        self.p_spectrum: np.ndarray = None

        self.kernel_size: int = None
        self.t_spectrum_smooth: np.ndarray = None
        self.rF_spectrum_smooth: np.ndarray = None
        self.p_spectrum_smooth: np.ndarray = None
        
        self.parse_expe(fn, self.start_time, self.end_time)
        self.detrend_signal()
        self.calc_spectrum()
        self.smooth_1d_arr()
        
        print(f"Processing date {self.date}")
    
    def parse_expe(self, fn: str, start_time: str, end_time: str) -> None:
    
        df = pd.read_csv(fn, delimiter=";")

        sensor0 = df.loc[df['Module Command'] == 0]
        rename_cols = {"Value2":"T", "Value3":"rF", "Value4":"p"}
        type_cols = {'T': float, 'rF': float, 'p': float}
        sensor0 = sensor0.rename(columns=rename_cols).astype(type_cols)

        sensor0["T"] = sensor0["T"]/100
        sensor0["rF"] = sensor0["rF"]/1000
        sensor0["p"] = sensor0["p"]/1000

        sensor0["Datetime"] = sensor0['Date'].astype(str) +" "+ sensor0["Time"]
        
        sensor0["Datetime"] = pd.to_datetime(sensor0["Datetime"], format="%Y-%m-%d %H:%M:%S")
        sensor0_flt = sensor0.loc[sensor0['Datetime'].between(start_time, end_time, inclusive="both")]

        if len(sensor0_flt) == 0:
            sys.exit(f"Temporal filtering of {self.fn} results in 0 data points.")

        self.time_raw = pd.to_datetime(sensor0_flt["Datetime"])
        self.t_raw = sensor0_flt["T"].to_numpy()
        self.rF_raw = sensor0_flt["rF"].to_numpy()
        self.p_raw = sensor0_flt["p"].to_numpy()

    def detrend_signal(self) -> None:
        self.t_det = np.mean(self.t_raw) + detrend(self.t_raw, type="linear")
        self.rF_det = np.mean(self.rF_raw) + detrend(self.rF_raw, type="linear")
        self.p_det = np.mean(self.p_raw) + detrend(self.p_raw, type="linear")

    def calc_spectrum(self, sample_rate: int = 1) -> None:

        # Calculate FFT        
        fft_output = fft.fft(self.t_det)
        self.freqs_t = fft.fftfreq(len(self.t_det), 1/sample_rate)
        self.spectrum_t = np.abs(fft_output)

        fft_output = fft.fft(self.rF_det)
        self.freqs_rF = fft.fftfreq(len(self.rF_det), 1/sample_rate)
        self.spectrum_rF = np.abs(fft_output)

        fft_output = fft.fft(self.p_det)
        self.freqs_p = fft.fftfreq(len(self.p_det), 1/sample_rate)
        self.spectrum_p = np.abs(fft_output)
        
        # Remove frequencies above Nyquist frequency
        self.nf = floor(len(self.time_raw)/2)
        self.freqs_t = self.freqs_t[:self.nf]
        self.freqs_rF = self.freqs_rF[:self.nf]
        self.freqs_p = self.freqs_p[:self.nf]
        self.spectrum_t = self.spectrum_t[:self.nf]
        self.spectrum_rF = self.spectrum_rF[:self.nf]
        self.spectrum_p = self.spectrum_p[:self.nf]
      
    def smooth_1d_arr(self):
        self.kernel_size = 12
        kernel = np.ones(self.kernel_size) / self.kernel_size
        self.t_spectrum_smooth = np.convolve(self.spectrum_t, kernel, mode='valid')
        self.rF_spectrum_smooth = np.convolve(self.spectrum_rF, kernel, mode='valid')
        self.p_spectrum_smooth = np.convolve(self.spectrum_p, kernel, mode='valid')
        
        
fns = [ 
    "data/2023_07_08/20230708-1329-Log.txt",
    "data/2023_07_11/20230711-0504-Log.txt"
    ]

datasets = [
    ExpeDataset(fn=fns[0], start_time='2023-07-08 14:00:00', end_time='2023-07-08 15:00:00'),
    ExpeDataset(fn=fns[1], start_time='2023-07-11 10:00:00', end_time='2023-07-11 11:00:00')
]


fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(18,7))

for col_i in [0,1]:
    ds = datasets[col_i]

    # time series
    ax[0,col_i].plot(ds.time_raw, ds.t_raw, label="raw")
    ax[0,col_i].plot(ds.time_raw, ds.t_det, label="detrended")
    
    # spectrum
    ax[1,col_i].plot(ds.freqs_t, ds.spectrum_t, c="b", linewidth=0.5, alpha=0.5, label="raw spectrum")
    ax[1,col_i].scatter(ds.freqs_t, ds.spectrum_t, c="b", s=1, alpha=0.3)
    
    # smoooth spectrum
    cutoff = int(ds.kernel_size/2)
    ax[1, col_i].plot(ds.freqs_t[cutoff:len(ds.freqs_t)-cutoff+1], ds.t_spectrum_smooth, c="r", linewidth=1, label="smooth spectrum")
    
    # plot area between 1 min and 10 min
    ax[1, col_i].axvspan(1/60, 1/600, alpha=0.1, color="grey", label="1 min - 10 min")
    
    # plot setup
    
    ## labels
    ax[0,col_i].set_title(f"Date: {ds.date}")
    ax[0,col_i].set_xlabel("Time [CET]")
    ax[0,col_i].set_ylabel("Temperature [°C]")
    ax[1,col_i].set_xlabel("Frequency [Hz]")
    ax[1,col_i].set_ylabel("Magnitude Spectrum")

    ## scale
    ax[1,col_i].set_yscale("log")
    # ax[1,col_i].set_xscale("log")    

    ## limits
    ax[1, col_i].set_xlim(0, 0.5)
    ax[1, col_i].set_ylim(1e-2, 1e5)
    ax[0, col_i].set_ylim(20, 45)
    
    ## primary x tick labels
    ax[0,col_i].xaxis.set_major_formatter(DateFormatter('%H:%M'))
    
    ## secondary x tick labels
    ax2 = ax[1,col_i].twiny()
    ax2.set_xlim(ax[1,col_i].get_xlim())
    ax2.set_xticks(ax[1,col_i].get_xticks())
    ax2.set_xticklabels(np.round(1/ax[1,col_i].get_xticks(), 2))
    ax2.xaxis.set_ticks_position("bottom")
    ax2.xaxis.set_label_position("bottom")
    ax2.spines["bottom"].set_position(("axes", -0.2))
    ax2.set_xlabel("Period [s]")
    
    ## grid and legend
    for row_i in [0, 1]:
        ax[row_i, col_i].grid(True)
        ax[row_i,col_i].legend()

    
plt.tight_layout()
plt.savefig("images/FFT.png", dpi=300, bbox_inches="tight")
plt.close()





exit(1)    


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))

for i in [0,1]:
    
    freqs, spectrum = calc_spectrum(signal=data["T"].tolist(), sample_rate=1)
    
    
    
    
    

plt.savefig("hist_new.png", dpi=300)