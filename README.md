Made as part of the course "MHYD11 Vertiefungspraxis Meteorologie" at TU Dresden.

## Content
- `data/` contains the raw data sorted by measuring date
- `results/` contains the results of the analysis
- `src/` contains the source code

## Usage
1. Clone the repository
```bash
git clone git@github.com:lenamueller/turbulenzspektren.git
```
2. Install the required python packages
```bash
pip install -r requirements.txt
```
3. Run the analysis script containing plotting the temporal coverage, the turbulence spectrum and the averaging
```bash
source src/Python_3_11_3/run_analysis.sh
```
## Dependencies
See `requirements.txt`

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
![temporal_coverage.png](results/temporal_coverage.png)