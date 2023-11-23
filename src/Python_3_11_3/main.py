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
# calculations
# -----------------------------------------------------------------------------

print("Run calculations...")

for period in all_puos:
    for device in ["SONIC", "EXPE"]:
        print(period, device)
        data = parse_data(device, period)
        
        match device:
            case "EXPE":
                
                # load data
                dt = data["Datetime"].to_numpy()
                t = data["t"].to_numpy()
                rh = data["rh"].to_numpy()
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
                
                # calculate turbulence intensity
                for var in ["t", "rh", "p"]:
                    print(f"\t\tTurbulent intensity of {var}: {calc_turb_int(y=timeseries_data[var])}")
            
            case "SONIC":

                # load data
                dt = data["Datetime"].to_numpy()
                t = data["t"].to_numpy()
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

                # calculate turbulence intensity
                for var in ["t", "wind3d", "wind2d"]:
                    print(f"\t\tTurbulent intensity of {var}: {calc_turb_int(y=timeseries_data[var])}")
                    
for period in all_puos:
    comparison = pd.DataFrame()    
    
    # EXPE
    data = parse_data("EXPE", period)
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    rh = data["rh"].to_numpy()
    p = data["p"].to_numpy()
    
    comparison["frequencies"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[0]
    n_expe = len(comparison)
    
    comparison["EXPE_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[1]
    comparison["EXPE_rh"] = calc_spectrum(dt, taper_signal(detrend_signal(rh), perc=0.1))[1]
    comparison["EXPE_p"] = calc_spectrum(dt, taper_signal(detrend_signal(p), perc=0.1))[1]
    
    # SONIC
    data = parse_data("SONIC", period)
    
    dt = data["Datetime"].to_numpy()
    t = data["t"].to_numpy()
    wind3d = data["wind3d"].to_numpy()
    wind2d = data["wind2d"].to_numpy()
    
    comparison["SONIC_t"] = calc_spectrum(dt, taper_signal(detrend_signal(t), perc=0.1))[1][:n_expe]
    comparison["SONIC_wind3d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind3d), perc=0.1))[1][:n_expe]
    comparison["SONIC_wind2d"] = calc_spectrum(dt, taper_signal(detrend_signal(wind2d), perc=0.1))[1][:n_expe]
        
    # save to csv
    comparison.to_csv(f"data/spectra_data/comparison_{period}.csv", index=False)
        
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