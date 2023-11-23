This repository contains data and code for analyzing the turbulence spectrum of meteorological data (part of the course "MHYD11 Vertiefungspraxis Meteorologie" at TU Dresden). The data was collected using two measuring devices (EXPE and SONIC) during summer (08.07.2023 - 14.08.2023). 

- EXPE: device measuring temperature, relative humidity and pressure as well as GPS information (lat, lon, elev) and time (UTC). Files are stored as `YYYYMMDD-HHMM-Log.txt`.
- SONIC: device measuring wind speed components (x, y, z), temperature and time (UTC+1, without daylight saving time). Files are stored as `TOA5_*.Raw_YYYY_MM_DD_*.dat`.

# Usage
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

# Content

`data/`
- `raw_data/YYYY_MM_DD/` contains the raw data by measuring date as txt-files
- `spectra_data/` contains the spectra data as csv-files
- `timeseries_data/ contains the time series data (raw, detrended, tapered) as csv-files`

``src/Python_3_11_3/``
- `main.py` runs the analysis
- `setup.py` contains the setup of the analysis (paths, global variables etc.)
- `parse.py` parses the raw data
    - ``data = parse_data(device, period)`` parses the raw data from two devices
    ("EXPE" or "SONIC") and a given time period. Expe variables are Datetime, 
    Temperature, relative Humidity and Pressure. Sonic variables are Datetime, 
    2D Wind, 3D Wind and Temerature.
    - ``data = get_var(device, period, var)`` returns the variable of a given device and time period
- `process.py` <mark> processes the data </mark>
    - ``n = sample_size(x)`` calculates the sample size of the data
    - ``sr = sample_rate(x)`` calculates the sample rate of the data
    - ``freq = sample_freq(x)`` calculates the sample frequencies of the data
    - ``y_det = detrend_signal(y)`` detrends the data
    - ``y_tap = taper_signal(y, func, perc)`` tapers x percentage of the data
    - ``freq, spectrum = calc_spectrum(y)`` calculates the spectrum of the data
    - ``x, y_mean = roll_mean(y, win_len)`` calculates the rolling mean of the spectrum
    - ``x, y_mean = step_mean(y, win_len)`` calculates the step mean of the spectrum
    - ``y_norm = min_max_norm(y)`` calculates the min-max-normalization of the data
- `plot.py` plots the data


`plots/` contains the plots created with `plot.py`

# Periods under observation
This plot shows the temporal coverage of the experiments. The highlighted area shows the periods under investigation, which are free from measurement errors and both EXPE and SONIC data are available.

<img src="plots/temporal_coverage/temporal_coverage.png" alt="plots/temporal_coverage/temporal_coverage.png" width="800"/>

## Example plots for measuring device EXPE and period under investigation 11.08.2023 morning (PUO_05)

#### `plots/preprocessing/`
This plot shows the raw signal (top), the detrended signal (middle) and the tapered signal (bottom, default tapering function is cosine) of the temperature time series of the EXPE device on 11.08.2023 morning.

<img src="plots/preprocessing/preprocess_PUO_05_EXPE_t.png" alt="plots/preprocessing/preprocess_PUO_05_EXPE_t.png" width="600"/>   


#### `plots/averaging/`
This plot shows the detrended signal (top), the rolling mean with different window sizes (middle) and the resulting fluctuations (bottom) of the temperature time series of the EXPE device on 11.08.2023 morning.

<img src="plots/averaging/avg_PUO_05_EXPE_t.png" alt="plots/averaging/avg_PUO_05_EXPE_t.png" width="600"/>

#### `plots/spectra/`
This plot shows the tapered signal (top) and the spectrum (middle, grey: calculated, red: smoothed with rolling mean) of the temperature time series of the EXPE device on 11.08.2023 morning. The highlighted area shows the period range from 30 to 60 minutes, where a spectral gap is expected for meteoroogical data.

<img src="plots/spectra/spec_PUO_05_EXPE_t.png" alt="plots/spectra/spec_PUO_05_EXPE_t.png" width="600"/>

#### `plots/spectra_comparison/`

This plot shows the comparison of all spectra of the periods under investigation of the temperature time series of the EXPE device.

<img src="plots/spectra_comparison/spectra_temporal_comparison_EXPE_SONIC_t.png" alt="spectra_temporal_comparison_EXPE_SONIC_t.png" width="800"/>

This plot compares the normalized spectra of different variables for the period under investigation.

<img src="plots/spectra_comparison/spectra_variable_comparison_PUO_05.png" alt="" width=600>

#### `plots/sensitivity_wf`
This plot shows the non-parametric window functions.
The blue function shows the window function only applied to the first and last 10 % of the data. boxcar function is a rectangular window (equivalient to no window at all).

<img src="plots/sensitivity_wf/window_functions.png" alt="windpw_functions.png" width="600"/>

This plot shows the (relatively small) influence of the window functions on the spectrum of the temperature time series of the EXPE device on 11.08.2023 morning.

<img src="plots/sensitivity_wf/wf_PUO_05_EXPE_t.png" alt="wf_PUO_05_EXPE_t.png" width="600"/>


