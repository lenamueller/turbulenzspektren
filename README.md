Made as part of the course "MHYD11 Vertiefungspraxis Meteorologie" at TU Dresden.

# Content
## `data/`
`YYYY_MM_DD/` contains the raw data sorted by measuring date

`spectra_data/` contains the spectra data

`timeseries_data/` contains the time series data (raw, detrended, tapered)

## `results/`
contains the results of the analysis

## `src/Python_3_11_3`
contains the Python source code

### `main.py`

### `parse.py` 
- ``data = parse_data(device, period)`` parses the raw data from two devices
("EXPE" or "SONIC") and a given time period. Expe variables are Datetime, 
Temperature, relative Humidity and Pressure. Sonic variables are Datetime, 
2D Wind, 3D Wind and Temerature.

### `process.py` processes the data 
- ``n = sample_size(x)`` calculates the sample size of the data
- ``sr = sample_rate(x)`` calculates the sample rate of the data
- ``freq = sample_freq(x)`` calculates the sample frequencies of the data
- ``y_det = detrend_signal(y)`` detrends the data
- ``y_tap = taper_signal(y, func, perc)`` tapers x percentage of the data
- ``freq, spectrum = calc_spectrum(y)`` calculates the spectrum of the data
- ``y_smo = smooth(x, y, win_len)`` smooths the spectrum
- ``x, y_mean = roll_mean(y, win_len)`` calculates the rolling mean of the spectrum
- ``x, y_mean = step_mean(y, win_len)`` calculates the step mean of the spectrum
- ``y_norm = min_max_norm(y)`` calculates the min-max-normalization of the data

### `plot.py` plots the data
- ``plot_ts(x, y, fn, title)`` plots the processing steps of the time series
- ``plot_spectrum(x, y, fn, ylabel, title)`` plots the spectrum (with smoothing) of a time series
- ``plot_spectrum_comp(device)`` plots a comparison of all smoothed spectra
- ``plot_avg(todo)`` plots the average of a time series
- ``plot_win()`` plots the nonparametric window functions
- ``plot_win_influcence(x, y, subtitle, fn)`` plots the influence of the window function
- ``plot_temporal_coverage(todo)`` plots the temporal coverage of the experiments


### `setup.py`

## Usage
1. Clone the repository
```bash
git clone git@github.com:lenamueller/turbulenzspektren.git
```
2. Install the required python packages
```bash
pip install -r requirements.txt
```
3. Run the analysis script
```bash
python src/Python_3_11_3/main.py
```

## Measuring devices
1. Sonic Anemometer:
    - time: UTC+1, without daylight saving time
    - variables: 3D wind speed, temperature
    - filename format: `TOA5_*.Raw_YYYY_MM_DD_*.dat`
2. Expe module:
    - time: UTC
    - variables: temperature, relative humidity, pressure
    - filename format: `YYYYMMDD-HHMM-Log.txt`

## Temporary coverage of the data
![temporal_coverage.png](results/temporal_coverage/temporal_coverage.png)