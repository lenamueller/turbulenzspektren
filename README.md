## data
measurements of wind, temperature, rel. humidity and pressure (Sonic Anemometer and Expe module) in Dresden, Germany [2023]

## structure
- `data/` contains the raw data
- `results/` contains the results of the analysis
- `src/` contains the source code


## processing steps
1. parse expe and sonic data
2. detrend time series data
3. calculate FFT
4. calculate averaging errors (for window sizes of 1, 2, 3, 5, 10, 15, 30 minutes)
