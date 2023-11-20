""" 
File: main.py
Author: Lena Müller
Date: November 20, 2023

Description: Main file for running the analysis.
"""

import pandas as pd

from setup import metadata, all_puos
from parse import parse_data
from process import *
from plot import plot_ts, plot_spectrum, plot_spectrum_comp, plot_win


period = "PUO_01"
device = "EXPE"


plot_win()

for device in ["EXPE", "SONIC"]:
    plot_spectrum_comp(device)


for period in all_puos:
    _, _, start_datetime, end_datetime, date, _ = metadata(period)
    
    for device in ["EXPE", "SONIC"]:
        data = parse_data(device, period)

        match device:
            case "EXPE":
                
                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                rh = data["rH"].to_numpy()
                p = data["p"].to_numpy()
                
                # plot preprocessing
                plot_ts(dt, t, f"{period}_{device}_t",
                        title = f"Temperature [°C]\n\n {date} ({device}, 1 Hz)\n")
                plot_ts(dt, rh, f"{period}_{device}_rh",
                        title = f"Relative Humidiity [%] \n\n {date} ({device}, 1 Hz)\n")
                plot_ts(dt, p, f"{period}_{device}_p", 
                        title = f"Pressure [hPa]\n\n {date} ({device}, 1 Hz)\n")
                
                # save spectra data                
                fft_data = {}
                fft_data["frequencies"] = sample_freq(dt)
                fft_data["spectrum_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), 0.1))[1]
                fft_data["spectrum_rh"] = calc_spectrum(dt, taper_signal(detrend_signal(rh), 0.1))[1]
                fft_data["spectrum_p"] = calc_spectrum(dt, taper_signal(detrend_signal(p), 0.1))[1]
                pd.DataFrame.from_dict(fft_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)
                
                # plot spectra            
                plot_spectrum(dt, t, f"{period}_{device}_t", "Temperature [°C]",
                        title = f"Temperature [°C]\n\n {date} ({device}, 1 Hz)\n")
                plot_spectrum(dt, rh, f"{period}_{device}_rh", "Relative Humidiity [%]",
                        title = f"Relative Humidiity [%] \n\n {date} ({device}, 1 Hz)\n")
                plot_spectrum(dt, p, f"{period}_{device}_p", "Pressure [hPa]",
                        title = f"Pressure [hPa]\n\n {date} ({device}, 1 Hz)\n")
                
            case "SONIC":

                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                wind3d = data["wind3d"].to_numpy()
                wind2d = data["wind2d"].to_numpy()
                
                # plot preprocessing                
                plot_ts(dt, t, f"{period}_{device}_t",
                        title = f"Temperature [°C]\n\n {date} ({device}, 2 Hz)\n")
                plot_ts(dt, wind3d, f"{period}_{device}_rh", 
                        title = f"3D Wind [m/s] \n\n {date} ({device}, 2 Hz)\n")
                plot_ts(dt, wind2d, f"{period}_{device}_p", 
                        title = f"2D Wind [m/s]\n\n {date} ({device}, 2 Hz)\n")
                
                # save spectra data
                fft_data = {}
                fft_data["frequencies"] = sample_freq(dt)
                fft_data["spectrum_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), 0.1))[1]
                fft_data["spectrum_wind3d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind3d), 0.1))[1]
                fft_data["spectrum_wind2d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind2d), 0.1))[1]
                pd.DataFrame.from_dict(fft_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)
                
                # plot spectra
                plot_spectrum(dt, t, f"{period}_{device}_t", "Temperature [°C]",
                        title = f"Temperature [°C]\n\n {date} ({device}, 2 Hz)\n")
                plot_spectrum(dt, wind3d, f"{period}_{device}_rh", "3D Wind [m/s]",
                        title = f"3D Wind [m/s] \n\n {date} ({device}, 2 Hz)\n")
                plot_spectrum(dt, wind2d, f"{period}_{device}_p", "2D Wind [m/s]",
                        title = f"2D Wind [m/s]\n\n {date} ({device}, 2 Hz)\n")
                
