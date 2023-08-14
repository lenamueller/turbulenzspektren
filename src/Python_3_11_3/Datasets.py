import matplotlib.pyplot as plt
import sys
from math import floor
import numpy as np
import pandas as pd
from scipy import fft
from scipy.signal import detrend
from scipy.signal.windows import blackman, hamming, flattop, tukey, cosine, boxcar

pd.options.mode.chained_assignment = None  # default='warn'


class Dataset:
    """Base class for datasets"""
    def __init__(self, fn: str, start_time: str, end_time: str) -> None:
        
        self.fn: str = fn
        self.start_time: str = start_time
        self.end_time: str = end_time

        self.time_raw: np.ndarray = None
        self.nf: int = None # Nyquist frequency
        
    def parse_data() -> None:
        """empty method to be overwritten by subclasses """
        pass 

    def detrend_signal(self, var: np.ndarray) -> None:
        """Detrend the time series."""
        return np.mean(var) + detrend(var, type="linear")
    
    def calc_spectrum(self, var: np.ndarray, sample_rate: int = 1) -> None:
        """Calculate the FFT of the time series."""
        
        n = len(var)
        
        # Apply window function (tapering)
        var = tukey(M=len(var)) * var
        
        # 1D Discrete Fourier Transform
        fft_output = fft.fft(var)
        
        # Remove first element (mean) and frequencies above Nyquist frequency.
        fft_output = fft_output[1:n//2]
        
        # Discrete Fourier Transform sample frequencies
        freqs = fft.fftfreq(n, 1/sample_rate)[1:n//2]
        
        # Calculate the square of the norm of each complex number
        # Norm = sqrt(Re² + Im²)
        spectrum = np.square(np.abs(fft_output))

        # Multiply spectral energy density by frequency
        spectrum *= freqs
        
        # Multiply spectrum by 2 to account for negative frequencies
        spectrum = [i*2 for i in spectrum]
        
        return freqs, spectrum

    def smooth_spectrum(self, var: np.ndarray, kernel_size: int = 10) -> np.ndarray:
        """Smooth the time series with a moving average"""
        kernel = np.ones(kernel_size) / kernel_size
        return np.convolve(var, kernel, mode='valid')
        
    def step_mean(self, var: np.ndarray, window_size: int) -> list:
        """Calculate the average of the time series of variable var in intervals of x minutes."""
        l = []
        for i in range(0, len(self.time_raw), window_size):
            new_values = [np.mean(var[i:i+window_size])] * window_size
            l.extend(new_values)
        return l
        
    def rolling_mean(self, var: np.ndarray, window_size: int) -> list:
        """Calculate the rolling mean of the time series of variable var with a window_size of x minutes."""
        l = []
        for i in range(len(var)):
            if i < window_size:
                l.append(np.mean(var[0:i+1]))
            else:
                l.append(np.mean(var[i-window_size:i]))
        return l

class ExpeDataset(Dataset):
    """Dataset class for EXPE data"""

    def __init__(self, fn: str, start_time: str, end_time: str) -> None:
        super().__init__(fn, start_time, end_time)
        
        # temperature
        self.t_raw: np.ndarray = None
        self.t_det: np.ndarray = None
        self.t_freqs: np.ndarray = None
        self.t_spectrum: np.ndarray = None
        self.t_spectrum_smooth: np.ndarray = None

        # relative humidity
        self.rH_raw: np.ndarray = None
        self.rH_det: np.ndarray = None
        self.rH_freqs: np.ndarray = None
        self.rH_spectrum: np.ndarray = None
        self.rH_spectrum_smooth: np.ndarray = None
        
        # pressure
        self.p_raw: np.ndarray = None
        self.p_det: np.ndarray = None
        self.p_freqs: np.ndarray = None
        self.p_spectrum: np.ndarray = None
        self.p_spectrum_smooth: np.ndarray = None

        self.parse_data(fn, self.start_time, self.end_time)
        
        self.t_det = self.detrend_signal(var=self.t_raw)
        self.rH_det = self.detrend_signal(var=self.rH_raw)
        self.p_det = self.detrend_signal(var=self.p_raw)
        
        self.t_freqs, self.t_spectrum = self.calc_spectrum(var=self.t_det, sample_rate=1)
        self.rH_freqs, self.rH_spectrum = self.calc_spectrum(var=self.rH_det, sample_rate=1)
        self.p_freqs, self.p_spectrum = self.calc_spectrum(var=self.p_det, sample_rate=1)
        
        self.p_spectrum_smooth = self.smooth_spectrum(self.p_spectrum)
        self.t_spectrum_smooth = self.smooth_spectrum(self.t_spectrum)
        self.rH_spectrum_smooth = self.smooth_spectrum(self.rH_spectrum)
        
        
    def parse_data(self, fn: str, start_time: str, end_time: str) -> None:
        """Parse the data from the csv-file using sensor 0."""
    
        df = pd.read_csv(fn, delimiter=";")

        sensor0 = df.loc[df['Module Command'] == 0]
        rename_cols = {"Value2":"T", "Value3":"rH", "Value4":"p"}
        type_cols = {'T': float, 'rH': float, 'p': float}
        sensor0 = sensor0.rename(columns=rename_cols).astype(type_cols)

        sensor0["T"] = sensor0["T"]/100
        sensor0["rH"] = sensor0["rH"]/1000
        sensor0["p"] = sensor0["p"]/1000

        sensor0["Datetime"] = sensor0['Date'].astype(str) +" "+ sensor0["Time"]
        sensor0["Datetime"] = pd.to_datetime(sensor0["Datetime"], format="%Y-%m-%d %H:%M:%S")
        sensor0_flt = sensor0.loc[sensor0['Datetime'].between(start_time, end_time, inclusive="both")]

        if len(sensor0_flt) == 0:
            sys.exit(f"\tTemporal filtering of {self.fn} results in 0 data points.")

        self.time_raw = pd.to_datetime(sensor0_flt["Datetime"])
        self.t_raw = sensor0_flt["T"].to_numpy()
        self.rH_raw = sensor0_flt["rH"].to_numpy()
        self.p_raw = sensor0_flt["p"].to_numpy()
   

class SonicDataset(Dataset):
    """Dataset class for SONIC anemometer data"""

    def __init__(self, fn: str, start_time: str, end_time: str) -> None:
        super().__init__(fn, start_time, end_time)
        
        # wind
        self.windx_raw: np.ndarray = None
        self.windy_raw: np.ndarray = None
        self.windz_raw: np.ndarray = None
        
        self.wind3d: np.ndarray = None
        self.wind3d_det: np.ndarray = None
        self.wind3dfreqs: np.ndarray = None
        self.wind3d_spectrum: np.ndarray = None
        self.wind3d_spectrum_smooth: np.ndarray = None

        self.wind2d: np.ndarray = None
        self.wind2d_det: np.ndarray = None
        self.wind2dfreqs: np.ndarray = None
        self.wind2d_spectrum: np.ndarray = None
        self.wind2d_spectrum_smooth: np.ndarray = None
        
        # temperature
        self.t_raw: np.ndarray = None
        self.t_det: np.ndarray = None
        self.t_freqs: np.ndarray = None
        self.t_spectrum: np.ndarray = None
        self.t_spectrum_smooth: np.ndarray = None

        self.parse_data(fn, self.start_time, self.end_time)
        
        self.wind3d_det = self.detrend_signal(var=self.wind3d)
        self.wind2d_det = self.detrend_signal(var=self.wind2d)
        self.t_det = self.detrend_signal(var=self.t_raw)
        
        self.wind3d_freqs, self.wind3d_spectrum = self.calc_spectrum(var=self.wind3d_det, sample_rate=0.5)
        self.wind2d_freqs, self.wind2d_spectrum = self.calc_spectrum(var=self.wind2d_det, sample_rate=0.5)
        self.t_freqs, self.t_spectrum = self.calc_spectrum(var=self.wind3d_det, sample_rate=0.5)
        
        self.wind2d_spectrum_smooth = self.smooth_spectrum(self.wind2d_spectrum)
        self.wind3d_spectrum_smooth = self.smooth_spectrum(self.wind3d_spectrum)
        self.t_spectrum_smooth = self.smooth_spectrum(self.t_spectrum)
        
    def parse_data(self, fn: str, start_time: str, end_time: str) -> None:
        """Parse the data from the dat-file and calculate 2D and 3D wind speed."""
        df = pd.read_csv(fn, delimiter=",", usecols=[0,2,3,4,5], names=["Datetime", "windx", "windy", "windz", "T"], skiprows=4)    
        type_cols = {'windx': float, 'windy': float, 'windz': float, 'T': float}
        df = df.astype(type_cols)
        df = df.dropna()
        
        # Convert local time (wihout summer time) to UTC
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y-%m-%d %H:%M:%S")
        df["Datetime"] = df["Datetime"] - pd.Timedelta(hours=1)
        
        df_flt = df.loc[df['Datetime'].between(start_time, end_time, inclusive="both")]
        if len(df_flt) == 0:
            sys.exit(f"\tTemporal filtering of {self.fn} results in 0 data points.")

        def calc_3d_wind(row)-> float:
            """Calculate the absolute wind speed from the 3 wind components."""
            return np.sqrt(row["windx"]**2 + row["windy"]**2 + row["windz"]**2)
        
        def calc_2d_wind(row)-> float:
            """Calculate the horizontal wind speed from the 3 wind components."""
            return np.sqrt(row["windx"]**2 + row["windy"]**2)
        
        df_flt.loc[:, "wind3d"] = df_flt.apply(calc_3d_wind, axis=1)
        df_flt.loc[:, "wind2d"] = df_flt.apply(calc_2d_wind, axis=1)

        self.time_raw = pd.to_datetime(df_flt["Datetime"])
        self.windx_raw = df_flt["windx"].to_numpy()
        self.windy_raw = df_flt["windy"].to_numpy()
        self.windz_raw = df_flt["windz"].to_numpy()
        self.wind3d = df_flt["wind3d"].to_numpy()
        self.wind2d = df_flt["wind2d"].to_numpy()
        self.t_raw = df_flt["T"].to_numpy()
