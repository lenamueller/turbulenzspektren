import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from setup import KERNEL_SIZE, TAPERING_SIZE, SAMPLE_RATE, variables, labels, all_puos, metadata
from parse import parse_data, get_var
from process import detrend_signal, taper_signal, sample_freq, calc_spectrum, roll_mean, \
    calc_turb_int

from plot import plot_ts, plot_spectrum, plot_spectrum_comp, plot_t_spectrum_comp, plot_win, \
    plot_win_influence, plot_avg, plot_temporal_coverage, plot_turbulent_intensity, plot_patterns, \
    plot_corr


# -----------------------------------------------------------------------------
# process EXPE data
# -----------------------------------------------------------------------------

print("Process EXPE data...")
for period in all_puos:

    # load data
    data = parse_data("EXPE", period)
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    
    # calculate detrended and tapered time series
    timeseries_data = {}
    timeseries_data["datetime"] = dt
    timeseries_data["t"] = t
    timeseries_data["t_det"] = detrend_signal(t)
    timeseries_data["t_tap"] = taper_signal(timeseries_data["t_det"], TAPERING_SIZE)
    
    pd.DataFrame.from_dict(timeseries_data).to_csv(
        f"data/timeseries_data/{period}_EXPE_preprocessed_data.csv", index=False)
    
    # calculate spectrum and smooth it with rolling mean
    spectrum_data = {}
    spectrum_data["frequencies"] = sample_freq(dt)
    spectrum_data["t_spec"] = calc_spectrum(dt, timeseries_data["t_tap"])[1]
    spectrum_data["t_spec_smooth"] = roll_mean(spectrum_data["t_spec"], win_len=KERNEL_SIZE)
    
    pd.DataFrame.from_dict(spectrum_data).to_csv(
            f"data/spectra_data/{period}_EXPE_spectrum_data.csv", index=False)

# -----------------------------------------------------------------------------
# process SONIC data
# -----------------------------------------------------------------------------

print("Process SONIC data...")
for period in all_puos:
    
    # load data
    data = parse_data("SONIC", period)
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    wind_z = data["wind_z"].to_numpy()
    wind_h = data["wind_h"].to_numpy()
    
    # calculate detrended and tapered time series
    timeseries_data = {}
    timeseries_data["datetime"] = dt
    
    timeseries_data["t"] = t
    timeseries_data["t_det"] = detrend_signal(t)
    timeseries_data["t_tap"] = taper_signal(timeseries_data["t_det"], TAPERING_SIZE)
    
    timeseries_data["wind_z"] = wind_z
    timeseries_data["wind_z_det"] = detrend_signal(wind_z)
    timeseries_data["wind_z_tap"] = taper_signal(timeseries_data["wind_z_det"], TAPERING_SIZE)
    
    timeseries_data["wind_h"] = wind_h
    timeseries_data["wind_h_det"] = detrend_signal(wind_h)
    timeseries_data["wind_h_tap"] = taper_signal(timeseries_data["wind_h_det"], TAPERING_SIZE)
    
    pd.DataFrame.from_dict(timeseries_data).to_csv(
        f"data/timeseries_data/{period}_SONIC_preprocessed_data.csv", index=False)
    
    # calculate spectrum and smooth it with rolling mean
    spectrum_data = {}
    spectrum_data["frequencies"] = sample_freq(dt)
    
    spectrum_data["t_spec"] = calc_spectrum(dt, timeseries_data["t_tap"])[1]
    spectrum_data["t_spec_smooth"] = roll_mean(spectrum_data["t_spec"], win_len=KERNEL_SIZE)
    
    spectrum_data["wind_z_spec"] = calc_spectrum(dt, timeseries_data["wind_z_tap"])[1]
    spectrum_data["wind_z_spec_smooth"] = roll_mean(spectrum_data["wind_z_spec"], win_len=KERNEL_SIZE)
    
    spectrum_data["wind_h_spec"] = calc_spectrum(dt, timeseries_data["wind_h_tap"])[1]
    spectrum_data["wind_h_spec_smooth"] = roll_mean(spectrum_data["wind_h_spec"], win_len=KERNEL_SIZE)
    
    pd.DataFrame.from_dict(spectrum_data).to_csv(
            f"data/spectra_data/{period}_SONIC_spectrum_data.csv", index=False)

# -----------------------------------------------------------------------------
# process EXPE and SONIC data and store them in one file
# -----------------------------------------------------------------------------

print("Process EXPE and SONIC data...")
for period in all_puos:
    
    comparison = pd.DataFrame()    
    
    # EXPE
    data = parse_data("EXPE", period)
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    
    comparison["frequencies"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[0]
    comparison["EXPE_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[1]
    
    n_expe = len(comparison)
    
    # SONIC
    data = parse_data("SONIC", period)
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    wind_z = data["wind_z"].to_numpy()
    wind_h = data["wind_h"].to_numpy()
    
    comparison["SONIC_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[1][:n_expe]
    comparison["SONIC_wind_z"] = calc_spectrum(dt, taper_signal(detrend_signal(wind_z), perc=0.1))[1][:n_expe]
    comparison["SONIC_wind_h"] = calc_spectrum(dt, taper_signal(detrend_signal(wind_h), perc=0.1))[1][:n_expe]
        
    # save to csv
    comparison.to_csv(f"data/spectra_data/{period}_comparison_spectrum_data.csv", index=False)

        
# -----------------------------------------------------------------------------
# plotting
# -----------------------------------------------------------------------------

for period in all_puos:
    
    
    
    for device in ["EXPE", "SONIC"]:
        print("Run plotting - ", period, "&", device)
        
        expe_fn, sonic_fn, start_datetime, end_datetime, date, day = metadata(period)

        for var in variables[device]:
            l = labels[var]
            
            print("\t", l)
            
            suptitle_info = f"""{l}\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {SAMPLE_RATE[device]} Hz)"""
        
            print("\t\tPlotting time series preprocessing...")
            plot_ts(
                x=get_var(device, period, "Datetime"),
                y=get_var(device, period, var),
                fn=f"{period}_{device}_{var}", 
                title = suptitle_info
                )

            print("\t\tPlotting spectra...")
            plot_spectrum(
                x=get_var(device, period, "Datetime"),
                y=get_var(device, period, var),
                fn=f"{period}_{device}_{var}",
                ylabel=l, 
                title = suptitle_info
                )
            
            print("\t\tPlotting averaging...")
            plot_avg(
                x=get_var(device, period, "Datetime"),
                y=get_var(device, period, var),
                device=device,
                title=suptitle_info,
                fn=f"avg_{period}_{device}_{var}"
                )
            
            plot_win_influence(
                x=get_var(device, period, "Datetime"),
                y=get_var(device, period, var),
                title=suptitle_info,
                fn=f"wf_{period}_{device}_{var}"
            )


# temporal coverage
plot_temporal_coverage()

# spectra comparison
plot_spectrum_comp("EXPE")
plot_spectrum_comp("SONIC")
plot_t_spectrum_comp()

# spectra patterns
for period in all_puos:
    plot_patterns(period)

# spectra correlation
plot_corr()

# window functions
plot_win()

# turbulent intensity
plot_turbulent_intensity()

print("Done.")