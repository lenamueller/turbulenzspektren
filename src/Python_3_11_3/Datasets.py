"""
File: Datasets.py
Author: Lena Müller
Date: November 14, 2023

Description:
This module defines the Dataset class and its subclasses, which provide methods 
for parsing and processing time series data. The Dataset class is a base class 
that defines common methods for all datasets, while the ExpeDataset class and
the SonicDataset class are subclasses with parsing functions and individual 
attributes.

Classes:
- Dataset: Base class for datasets.
- ExpeDataset: Dataset class for EXPE data.
- SonicDataset: Dataset class for SONIC anemometer data.
"""

import numpy as np
import pandas as pd
import scipy

pd.options.mode.chained_assignment = None  # default='warn'

from setup import metadata


class Dataset:
    """Base class for datasets"""
    def __init__(self, puo: str) -> None:
        
        expe_fn, sonic_fn, start_datetime, end_datetime, date, day = metadata(puo)
        
        # file names of raw data
        self.expe_fn = expe_fn
        self.sonic_fn = sonic_fn
        
        # measurement device
        self.mesuring_device: str = None
        
        # temporal meta data
        self.puo: str = puo
        self.start_datetime: str = start_datetime
        self.end_datetime: str = end_datetime
        self.date: str = date
        self.day: int = day
        
        # Time series
        self.time_raw: np.ndarray = None
        
        # Sample size
        self.n: int = None
        
        # Sample rate [1/Hz]
        self.sr: float = None
        
        # Sample frequencies
        self.freqs: np.ndarray = None
        
    def parse_data() -> None:
        """
        Parse raw data.
        (Empty method to be overwritten by subclasses)
        """
        pass 

    def detrend_signal(self, var: np.ndarray) -> None:
        """Detrend the time series."""
        return np.mean(var) + scipy.signal.detrend(var, type="linear")
    
    def sample_freqs(self, n: int, sample_rate: int = 1):
        """Return the sample frequencies of the time series."""
        return scipy.fft.fftfreq(n, 1/sample_rate)[1:n//2]
    
    def calc_spectrum(
            self,
            var: np.ndarray,
            sample_rate: int = 1,
            window: scipy.signal.windows = scipy.signal.windows.tukey,
            ) -> None:
        """Calculate the FFT of the time series."""
        
        n = len(var)
        
        # Apply window function
        # var = window(M=len(var)) * var
        
        # Apply winsow function to first and last 10% of the time series
        n_elem = int(0.1*self.n)
        var[:n_elem] = window(M=2*n_elem)[:n_elem] * var[:n_elem]
        var[self.n - n_elem:] = window(M=2*n_elem)[n_elem:] * var[self.n - n_elem:]
        
        # 1D Discrete Fourier Transform
        fft_output = scipy.fft.fft(var)
        
        # Remove first element (mean) and frequencies above Nyquist frequency.
        fft_output = fft_output[1:n//2]
        
        # Discrete Fourier Transform sample frequencies
        freqs = scipy.fft.fftfreq(n, 1/sample_rate)[1:n//2]
        
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
        """
        Calculate the average of the time series of variable var in 
        intervals of x minutes.
        """
        l = []
        for i in range(0, len(self.time_raw), window_size):
            new_values = [np.mean(var[i:i+window_size])] * window_size
            l.extend(new_values)
        return l
        
    def rolling_mean(self, var: np.ndarray, window_size: int) -> list:
        """
        Calculate the rolling mean of the time series of variable var with 
        a window_size of x minutes.
        """
        l = []
        for i in range(len(var)):
            if i < window_size:
                l.append(np.mean(var[0:i+1]))
            else:
                l.append(np.mean(var[i-window_size:i]))
        return l

    def save_spectrum_data(self):
        """
        Save spectrum data to csv-files. 
        (Empty method to be overwritten by subclasses)
        """
        pass

class ExpeDataset(Dataset):
    """Dataset class for EXPE data"""

    def __init__(self, puo: str) -> None:
        super().__init__(puo)
        
        # measurement device
        self.measuring_device: str = "EXPE"
        
        # Raw data
        self.parse_data(self.expe_fn, self.start_datetime, self.end_datetime)
        
        # Detrended data
        self.t_det = self.detrend_signal(var=self.t_raw)
        self.rH_det = self.detrend_signal(var=self.rH_raw)
        self.p_det = self.detrend_signal(var=self.p_raw)
        
        # Sample rate
        self.sr: float = 1 # 1 Hz

        # Sample frequencies
        self.freqs: np.ndarray = self.sample_freqs(n=len(self.time_raw), sample_rate=self.sr)
        
        # Spectrum
        _, self.t_spectrum = self.calc_spectrum(var=self.t_det, sample_rate=self.sr)
        _, self.rH_spectrum = self.calc_spectrum(var=self.rH_det, sample_rate=self.sr)
        _, self.p_spectrum = self.calc_spectrum(var=self.p_det, sample_rate=self.sr)
        
        # Smoothed spectrum
        self.p_spectrum_smooth = self.smooth_spectrum(self.p_spectrum)
        self.t_spectrum_smooth = self.smooth_spectrum(self.t_spectrum)
        self.rH_spectrum_smooth = self.smooth_spectrum(self.rH_spectrum)
        
    def parse_data(self, expe_fn: str, start_datetime: str, end_datetime: str) -> None:
        """Parse the data from the csv-file using sensor 0."""
        
        df = pd.read_csv(expe_fn, delimiter=";")

        sensor0 = df.loc[df['Module Command'] == 0]
        rename_cols = {"Value2":"T", "Value3":"rH", "Value4":"p"}
        type_cols = {'T': float, 'rH': float, 'p': float}
        sensor0 = sensor0.rename(columns=rename_cols).astype(type_cols)

        sensor0["T"] = sensor0["T"]/100
        sensor0["rH"] = sensor0["rH"]/1000
        sensor0["p"] = sensor0["p"]/1000

        sensor0["Datetime"] = sensor0['Date'].astype(str) +" "+ sensor0["Time"]
        sensor0["Datetime"] = pd.to_datetime(sensor0["Datetime"], format="%Y-%m-%d %H:%M:%S")
        sensor0_flt = sensor0.loc[sensor0['Datetime'].between(start_datetime, end_datetime, inclusive="both")]

        self.time_raw = pd.to_datetime(sensor0_flt["Datetime"])
        self.t_raw = sensor0_flt["T"].to_numpy()
        self.rH_raw = sensor0_flt["rH"].to_numpy()
        self.p_raw = sensor0_flt["p"].to_numpy()
        
        self.n = len(self.time_raw)
   
    def save_spectrum_data(self, fn: str):
        """Save the spectrum data to a csv file."""
        data = {
            "freqs": self.freqs,
            "t_spectrum": self.t_spectrum,
            "rH_spectrum": self.rH_spectrum,
            "p_spectrum": self.p_spectrum,
        }
        pd.DataFrame.from_dict(data).to_csv(fn, index=False)

class SonicDataset(Dataset):
    """Dataset class for SONIC anemometer data"""

    def __init__(self, puo: str) -> None:
        super().__init__(puo)
        
        # measurement device
        self.measuring_device: str = "SONIC"
        
        # Raw data
        self.parse_data(self.sonic_fn, self.start_datetime, self.end_datetime)
        
        # Detrended data
        self.wind3d_det = self.detrend_signal(var=self.wind3d)
        self.wind2d_det = self.detrend_signal(var=self.wind2d)
        self.t_det = self.detrend_signal(var=self.t_raw)
        
        # Sample rate
        self.sr: float = 0.5 # 2 Hz

        # Sample frequencies
        self.freqs = self.sample_freqs(n=len(self.time_raw), sample_rate=self.sr)
        
        # Spectrum
        _, self.wind3d_spectrum = self.calc_spectrum(var=self.wind3d_det, sample_rate=self.sr)
        _, self.wind2d_spectrum = self.calc_spectrum(var=self.wind2d_det, sample_rate=self.sr)
        _, self.t_spectrum = self.calc_spectrum(var=self.wind3d_det, sample_rate=self.sr)
        
        # Smoothed spectrum
        self.wind2d_spectrum_smooth = self.smooth_spectrum(self.wind2d_spectrum)
        self.wind3d_spectrum_smooth = self.smooth_spectrum(self.wind3d_spectrum)
        self.t_spectrum_smooth = self.smooth_spectrum(self.t_spectrum)
        
        
    def parse_data(self, sonic_fn: str, start_datetime: str, end_datetime: str) -> None:
        """Parse the data from the dat-file and calculate 2D and 3D wind speed."""
        
        df = pd.read_csv(sonic_fn, delimiter=",", usecols=[0,2,3,4,5], names=["Datetime", "windx", "windy", "windz", "T"], skiprows=4)    
        type_cols = {'windx': float, 'windy': float, 'windz': float, 'T': float}
        df = df.astype(type_cols)
        df = df.dropna()
        
        # Convert local time (wihout summer time) to UTC
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y-%m-%d %H:%M:%S")
        df["Datetime"] = df["Datetime"] - pd.Timedelta(hours=1)
        
        df_flt = df.loc[df['Datetime'].between(start_datetime, end_datetime, inclusive="both")]

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
        
        self.n = len(self.time_raw)

    def save_spectrum_data(self, fn: str):
        """Save the spectrum data to a csv file."""
        data = {
            "freqs": self.freqs,
            "wind3d_spectrum": self.wind3d_spectrum,
            "wind2d_spectrum": self.wind2d_spectrum,
            "t_spectrum": self.t_spectrum,
        }
        pd.DataFrame.from_dict(data).to_csv(fn, index=False)