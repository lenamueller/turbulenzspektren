""" 
File: main.py
Author: Lena Müller
Date: November 20, 2023

Description: Main file for running the analysis.
"""

import pandas as pd
pd.set_option("mode.chained_assignment", None)

from setup import KERNEL_SIZE, TAPERING_SIZE
from setup import metadata, all_puos, sample_rates
from parse import parse_data
from process import *
from plot import plot_ts, plot_spectrum, plot_spectrum_comp, plot_win, plot_win_influence, plot_avg


# -----------------------------------------------------------------------------
# calculations
# -----------------------------------------------------------------------------

print("Run calculations...")

for period in all_puos:
    for device in ["SONIC", "EXPE"]:
        
        data = parse_data(device, period)
        
        match device:
            case "EXPE":
                
                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                rh = data["rH"].to_numpy()
                p = data["p"].to_numpy()
                
                # time series data
                timeseries_data = {}
                timeseries_data["datetime"] = dt
                timeseries_data["t"] = t
                timeseries_data["rh"] = rh
                timeseries_data["p"] = p
                timeseries_data["t_det"] = detrend_signal(t)
                timeseries_data["rh_det"] = detrend_signal(rh)
                timeseries_data["p_det"] = detrend_signal(p)
                timeseries_data["t_tap"] = taper_signal(timeseries_data["t_det"], TAPERING_SIZE)
                timeseries_data["rh_tap"] = taper_signal(timeseries_data["rh_det"], TAPERING_SIZE)
                timeseries_data["p_tap"] = taper_signal(timeseries_data["p_det"], TAPERING_SIZE)
                pd.DataFrame.from_dict(timeseries_data).to_csv(
                    f"data/timeseries_data/{period}_{device}_preprocessed_data.csv", index=False)
                
                # spectrum data
                spectrum_data = {}
                spectrum_data["frequencies"] = sample_freq(dt)
                spectrum_data["t_spec"] = calc_spectrum(dt, timeseries_data["t_tap"])[1]
                spectrum_data["rh_spec"] = calc_spectrum(dt, timeseries_data["rh_tap"])[1]
                spectrum_data["p_spec"] = calc_spectrum(dt, timeseries_data["p_tap"])[1]
                spectrum_data["t_spec_smooth"] = roll_mean(spectrum_data["t_spec"], win_len=KERNEL_SIZE)
                spectrum_data["rh_spec_smooth"] = roll_mean(spectrum_data["rh_spec"], win_len=KERNEL_SIZE)
                spectrum_data["p_spec_smooth"] = roll_mean(spectrum_data["p_spec"], win_len=KERNEL_SIZE)
                pd.DataFrame.from_dict(spectrum_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)

            case "SONIC":

                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                wind3d = data["wind3d"].to_numpy()
                wind2d = data["wind2d"].to_numpy()
                
                # time series data
                timeseries_data = {}
                timeseries_data["datetime"] = dt
                timeseries_data["t"] = t
                timeseries_data["wind3d"] = wind3d
                timeseries_data["wind2d"] = wind2d
                timeseries_data["t_det"] = detrend_signal(t)
                timeseries_data["wind3d_det"] = detrend_signal(wind3d)
                timeseries_data["wind2d_det"] = detrend_signal(wind2d)
                timeseries_data["t_tap"] = taper_signal(timeseries_data["t_det"], TAPERING_SIZE)
                timeseries_data["wind3d_tap"] = taper_signal(timeseries_data["wind3d_det"], TAPERING_SIZE)
                timeseries_data["wind2d_tap"] = taper_signal(timeseries_data["wind2d_det"], TAPERING_SIZE)
                pd.DataFrame.from_dict(timeseries_data).to_csv(
                    f"data/timeseries_data/{period}_{device}_preprocessed_data.csv", index=False)
                
                # spectrum data
                spectrum_data = {}
                spectrum_data["frequencies"] = sample_freq(dt)
                spectrum_data["t_spec"] = calc_spectrum(dt, timeseries_data["t_tap"])[1]
                spectrum_data["wind3d_spec"] = calc_spectrum(dt, timeseries_data["wind3d_tap"])[1]
                spectrum_data["wind2d_spec"] = calc_spectrum(dt, timeseries_data["wind2d_tap"])[1]
                spectrum_data["t_spec_smooth"] = roll_mean(spectrum_data["t_spec"], win_len=KERNEL_SIZE)
                spectrum_data["wind3d_spec_smooth"] = roll_mean(spectrum_data["wind3d_spec"], win_len=KERNEL_SIZE)
                spectrum_data["wind2d_spec_smooth"] = roll_mean(spectrum_data["wind2d_spec"], win_len=KERNEL_SIZE)
                pd.DataFrame.from_dict(spectrum_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)

# -----------------------------------------------------------------------------
# plotting
# -----------------------------------------------------------------------------

print("Run plotting...")
exit()
plot_win()

for device in ["EXPE", "SONIC"]:
    plot_spectrum_comp(device)


for period in all_puos:
    expe_fn, sonic_fn, start_datetime, end_datetime, date, day = metadata(period)
    
    for device in ["SONIC", "EXPE"]:
        data = parse_data(device, period)
        
        match device:
            case "EXPE":
                
                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                rh = data["rH"].to_numpy()
                p = data["p"].to_numpy()

                subtitle_info = f"""\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {sample_rates[device]} Hz)"""

                # plot preprocessing
                plot_ts(dt, t, f"{period}_{device}_t",
                        title = "Temperature [°C]"+subtitle_info)
                plot_ts(dt, rh, f"{period}_{device}_rh",
                        title = "Relative Humidiity [%]"+subtitle_info)
                plot_ts(dt, p, f"{period}_{device}_p", 
                        title = "Pressure [hPa]"+subtitle_info)
                
                # save spectra data                
                spectrum_data = {}
                spectrum_data["frequencies"] = sample_freq(dt)
                spectrum_data["spectrum_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), 0.1))[1]
                spectrum_data["spectrum_rh"] = calc_spectrum(dt, taper_signal(detrend_signal(rh), 0.1))[1]
                spectrum_data["spectrum_p"] = calc_spectrum(dt, taper_signal(detrend_signal(p), 0.1))[1]
                pd.DataFrame.from_dict(spectrum_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)
                
                # plot spectra            
                plot_spectrum(dt, t, f"{period}_{device}_t", "Temperature [°C]",
                        title = "Temperature [°C]"+subtitle_info)
                plot_spectrum(dt, rh, f"{period}_{device}_rh", "Relative Humidiity [%]",
                        title = "Relative Humidiity [%]"+subtitle_info)
                plot_spectrum(dt, p, f"{period}_{device}_p", "Pressure [hPa]",
                        title = "Pressure [hPa]"+subtitle_info)
                
                # plot influence of window function
                plot_win_influence(dt, t, subtitle="Temperature [°C]"+subtitle_info, 
                                   fn=f"wf_{period}_{device}")
                plot_win_influence(dt, rh, subtitle=f"Relative Humidity [%]"+subtitle_info,
                                    fn=f"wf_{period}_{device}")
                plot_win_influence(dt, p, subtitle=f"Pressure [hPa]"+subtitle_info,
                                    fn=f"wf_{period}_{device}")
                
                # plot averaging
                plot_avg(dt, t, device, suptitle="Temperature [°C]"+subtitle_info,
                         fn=f"avg_{period}_{device}_t")
                plot_avg(dt, rh, device, suptitle="Relative Humidity [%]"+subtitle_info,
                            fn=f"avg_{period}_{device}_rh")
                plot_avg(dt, p, device, suptitle="Pressure [hPa]"+subtitle_info,
                            fn=f"avg_{period}_{device}_p")
                
            case "SONIC":

                # load data
                dt = data["Datetime"].to_numpy()
                t = data["T"].to_numpy()
                wind3d = data["wind3d"].to_numpy()
                wind2d = data["wind2d"].to_numpy()
                
                subtitle_info = f"""\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {sample_rates[device]} Hz)"""
                
                # plot preprocessing                
                plot_ts(dt, t, f"{period}_{device}_t",
                        title = "Temperature [°C]"+subtitle_info)
                plot_ts(dt, wind3d, f"{period}_{device}_rh", 
                        title = "3D Wind [m/s]"+subtitle_info)
                plot_ts(dt, wind2d, f"{period}_{device}_p", 
                        title = "2D Wind [m/s]"+subtitle_info)
                
                # save spectra data
                spectrum_data = {}
                spectrum_data["frequencies"] = sample_freq(dt)
                spectrum_data["spectrum_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), 0.1))[1]
                spectrum_data["spectrum_wind3d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind3d), 0.1))[1]
                spectrum_data["spectrum_wind2d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind2d), 0.1))[1]
                pd.DataFrame.from_dict(spectrum_data).to_csv(
                        f"data/spectra_data/{period}_{device}_spectrum_data.csv", index=False)
                
                # plot spectra
                plot_spectrum(dt, t, f"{period}_{device}_t", "Temperature [°C]",
                        title = "Temperature [°C]"+subtitle_info)
                plot_spectrum(dt, wind3d, f"{period}_{device}_rh", "3D Wind [m/s]",
                        title = "3D Wind [m/s]"+subtitle_info)
                plot_spectrum(dt, wind2d, f"{period}_{device}_p", "2D Wind [m/s]",
                        title = "2D Wind [m/s]"+subtitle_info)

                # plot influence of window function
                plot_win_influence(dt, t, subtitle=f"Temperature [°C]"+subtitle_info, 
                                   fn=f"wf_{period}_{device}")
                plot_win_influence(dt, wind3d, subtitle="3D Wind [m/s]"+subtitle_info,
                                    fn=f"wf_{period}_{device}")
                plot_win_influence(dt, wind2d, subtitle="2D Wind [m/s]"+subtitle_info,
                                    fn=f"wf_{period}_{device}")
                
                # plot averaging
                plot_avg(dt, t, device, suptitle="Temperature [°C]"+subtitle_info,
                         fn=f"avg_{period}_{device}_t")
                plot_avg(dt, wind3d, device, suptitle="3D Wind [m/s]"+subtitle_info,
                            fn=f"avg_{period}_{device}_wind3d")
                plot_avg(dt, wind2d, device, suptitle="2D Wind [m/s]"+subtitle_info,
                            fn=f"avg_{period}_{device}_wind2d")