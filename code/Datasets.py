import sys
from math import floor
import numpy as np
import pandas as pd
from scipy import fft
from scipy.signal import detrend

    
class ExpeDataset:
    def __init__(
            self, fn: str, 
            start_time: str,
            end_time: str) -> None:

        """Constructor"""

        # general
        self.date: str = fn[-21:-13]
        self.start_time: str = start_time
        self.end_time: str = end_time
        print(f"Processing EXPE data {self.date} {self.start_time} {self.end_time}")
        
        self.time_raw: np.ndarray = None
        self.nf: int = None
        self.kernel_size: int = None

        # temperature
        self.t_raw: np.ndarray = None
        self.t_det: np.ndarray = None
        self.t_freqs: np.ndarray = None
        self.t_spectrum: np.ndarray = None
        self.t_spectrum_smooth: np.ndarray = None

        # relative humidity
        self.rF_raw: np.ndarray = None
        self.rF_det: np.ndarray = None
        self.rF_freqs: np.ndarray = None
        self.rF_spectrum: np.ndarray = None
        self.rF_spectrum_smooth: np.ndarray = None

        # pressure
        self.p_raw: np.ndarray = None
        self.p_det: np.ndarray = None
        self.p_freqs: np.ndarray = None
        self.p_spectrum: np.ndarray = None
        self.p_spectrum_smooth: np.ndarray = None
        
        
        self.parse_data(fn, self.start_time, self.end_time)
        self.detrend_signal()
        self.calc_spectrum()
        self.smooth_1d_arr()
        
    def parse_data(self, fn: str, start_time: str, end_time: str) -> None:
        """Parse the data from the txt-file."""
    
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
        """Detrend the temperature, relative humidity and pressure time series."""
        self.t_det = np.mean(self.t_raw) + detrend(self.t_raw, type="linear")
        self.rF_det = np.mean(self.rF_raw) + detrend(self.rF_raw, type="linear")
        self.p_det = np.mean(self.p_raw) + detrend(self.p_raw, type="linear")

    def calc_spectrum(self, sample_rate: int = 1) -> None:
        """Calculate the FFT of the temperature, relative humidity and pressure time series."""

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
      
    def smooth_1d_arr(self) -> None:
        """Smooth the temperature, relative humidity and pressure spectrum with a moving average filter."""
        self.kernel_size = 12
        kernel = np.ones(self.kernel_size) / self.kernel_size
        self.t_spectrum_smooth = np.convolve(self.spectrum_t, kernel, mode='valid')
        self.rF_spectrum_smooth = np.convolve(self.spectrum_rF, kernel, mode='valid')
        self.p_spectrum_smooth = np.convolve(self.spectrum_p, kernel, mode='valid')

class SonicDataset():
    def __init__(self, fn: str, start_time: str, end_time: str) -> None:
        """Constructor"""

        self.date: str = fn[-21:-13]
        self.start_time: str = start_time
        self.end_time: str = end_time
        print(f"Processing SONIC data {self.date} {self.start_time} {self.end_time}")
        
        self.time_raw: np.ndarray = None
        
        # wind
        self.windx_raw: np.ndarray = None
        self.windy_raw: np.ndarray = None
        self.windz_raw: np.ndarray = None
        self.wind_total: np.ndarray = None
        self.wind_total_det: np.ndarray = None
        self.wind_freq: np.ndarray = None
        self.wind_spectrum: np.ndarray = None
        self.wind_spectrum_smooth: np.ndarray = None
        
        # temperature
        self.t_raw: np.ndarray = None
        self.t_det: np.ndarray = None
        self.t_freq: np.ndarray = None
        self.t_spectrum: np.ndarray = None
        self.t_spectrum_smooth: np.ndarray = None

        self.parse_data(fn, self.start_time, self.end_time)
        self.detrend_signal()
        self.calc_spectrum()
        self.smooth_1d_arr()
        
    def parse_data(self, fn: str, start_time: str, end_time: str) -> None:
        """Parse the data from the dat-file."""

        df = pd.read_csv(fn, delimiter=",", usecols=[0,2,3,4,5], names=["Datetime", "windx", "windy", "windz", "T"], skiprows=4)    
        
        type_cols = {'windx': float, 'windy': float, 'windz': float, 'T': float}
        df = df.astype(type_cols)
        
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y-%m-%d %H:%M:%S")
        df_flt = df.loc[df['Datetime'].between(start_time, end_time, inclusive="both")]
        if len(df_flt) == 0:
            sys.exit(f"Temporal filtering of {self.fn} results in 0 data points.")

        def calc_wind_total(row)-> float:
            """Calculate the absolute wind speed from the 3 wind components."""
            return np.sqrt(row["windx"]**2 + row["windy"]**2 + row["windz"]**2)
        
        df_flt["wind_total"] = df_flt.apply(calc_wind_total, axis=1)

        self.time_raw = pd.to_datetime(df_flt["Datetime"])
        self.windx_raw = df_flt["windx"].to_numpy()
        self.windy_raw = df_flt["windy"].to_numpy()
        self.windz_raw = df_flt["windz"].to_numpy()
        self.wind_total = df_flt["wind_total"].to_numpy()
        self.t_raw = df_flt["T"].to_numpy()
        
    def detrend_signal(self) -> None:
        """Detrend the wind and temperature time series."""
        self.wind_total_det = np.mean(self.wind_total) + detrend(self.wind_total, type="linear")
        self.t_det = np.mean(self.t_raw) + detrend(self.t_raw, type="linear")
    
    def calc_spectrum(self, sample_rate: int = 1) -> None:
        """Calculate the FFT of the wind and temperature time series."""
        
        # Calculate FFT for wind
        fft_output = fft.fft(self.wind_total_det)
        self.wind_freq = fft.fftfreq(len(self.wind_total_det), 1/sample_rate)
        self.wind_spectrum = np.abs(fft_output)
        
        # Calculate FFT for temperature
        fft_output = fft.fft(self.t_det)
        self.t_freq = fft.fftfreq(len(self.t_det), 1/sample_rate)
        self.t_spectrum = np.abs(fft_output)
        
        # Remove frequencies above Nyquist frequency
        self.nf = floor(len(self.time_raw)/2)
        self.wind_freq = self.wind_freq[:self.nf]
        self.wind_spectrum  = self.wind_spectrum[:self.nf]
        self.t_freq = self.t_freq[:self.nf]
        self.t_spectrum = self.t_spectrum[:self.nf]
        
    def smooth_1d_arr(self) -> None:
        """Smooth the wind and temperature spectrum with a moving average filter."""
        self.kernel_size = 12
        kernel = np.ones(self.kernel_size) / self.kernel_size
        self.wind_spectrum_smooth = np.convolve(self.wind_spectrum, kernel, mode='valid')
        self.t_spectrum_smooth = np.convolve(self.t_spectrum, kernel, mode='valid')
