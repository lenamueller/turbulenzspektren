import scipy 
import numpy as np


def sample_size(x: np.ndarray) -> int:
    """Return sample size."""
    n = len(x)
    return n

def sample_rate(x: np.ndarray) -> float: 
    """Return sample rate in Hz."""
    sr = float(np.timedelta64(1, 's') / (x[1] - x[0]))
    return sr

def sample_freq(x: np.ndarray) -> np.ndarray:
    """Return sample frequencies."""
    n = sample_size(x)
    sr = sample_rate(x)
    freq = scipy.fft.fftfreq(n, 1/sr)[1:n//2]
    return freq

def detrend_signal(y: np.ndarray) -> np.ndarray:
    """Detrend the signal."""
    y_det = scipy.signal.detrend(y, type="linear")
    return y_det

def taper_signal(
        y: np.ndarray,
        perc: float, 
        func: scipy.signal.windows = scipy.signal.windows.cosine
        ) -> np.ndarray:
    """Taper the signal.

    Args:
        y (np.ndarray): data
        func (scipy.signal.windows): window function
        perc (float): percentage of first and last values to tapered.
            Must be between 0 (no tapering) and 0.5 (full range).

    Returns:
        np.ndarray: tapered data
    """
    
    n = len(y)
    t_width = int(perc * len(y))
    
    if perc == 0.5:
        y_tap = func(M=len(y)) * y
    else:
        wf = func(M=2*t_width)
        scaling = np.ones(n)
        scaling[:t_width] = wf[:t_width]
        scaling[n-t_width:] = wf[t_width:]
        y_tap = scaling * y
    return y_tap

def calc_spectrum(x: np.ndarray, y: np.ndarray
                  ) -> tuple[np.ndarray, np.ndarray]:
    """Return the sample frequencies and spectrum of the signal."""
    
    # Sample size
    n = sample_size(x)
    
    # Discrete Fourier Transform sample frequencies
    freq = sample_freq(x)
    
    # 1D Discrete Fourier Transform
    fft_output = scipy.fft.fft(y)
    
    # Remove first element (mean) and frequencies above Nyquist frequency.
    fft_output = fft_output[1:n//2]
    
    # Calculate the square of the norm of each complex number
    spectrum = np.square(np.abs(fft_output))

    # Multiply spectral energy density by frequency
    spectrum *= freq
    
    # Multiply spectrum by 2 to account for negative frequencies
    spectrum = [i*2 for i in spectrum]
    
    return freq, spectrum

def roll_mean(y: np.ndarray, win_len: int
              ) -> np.ndarray:
    """Calculate the rolling mean of the time series (x, y) 
    using a window of length win_len."""
    y_mean = []
    for i in range(len(y)):
        if i < win_len:
            y_mean.append(np.mean(y[0:i+1]))
        else:
            y_mean.append(np.mean(y[i-win_len:i]))
    return y_mean

def step_mean(y: np.ndarray, win_len: int
              ) -> np.ndarray:
    """Calculate the step mean of the time series (x, y)
    using a window of length win_len."""
    y_mean = []
    for i in range(0, len(y), win_len):
        new_values = [np.mean(y[i:i+win_len])] * win_len
        y_mean.extend(new_values)
    return y_mean

def calc_turb_int(
        y: np.ndarray
        ) -> float:
    """Calculate the turbulence intensity of the signal."""
    ti: float = np.std(y) / np.mean(y)
    return ti