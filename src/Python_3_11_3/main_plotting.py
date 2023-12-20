import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from setup import SAMPLE_RATE, variables, labels, all_puos, metadata
from parse import get_var

from plot import plot_ts, plot_spectrum, plot_spectrum_comp, \
    plot_t_spectrum_comp, plot_win, plot_win_influence, plot_avg, \
    plot_temporal_coverage, plot_patterns, plot_mean_corr, \
    plot_turb_intensity, plot_wind_spectrum_comp, plot_error_metrics
    

# plotting agenda
PLOT_TEMPORAL_COVERAGE          = False
PLOT_TIME_SERIES                = False
PLOT_SPECTRUM_DATA              = False
PLOT_WINDOW_FUNCTION_INFLUENCE  = False
PLOT_AVERAGING                  = True
PLOT_TURBULENCE_INTENSITY       = False

TEST_MODE                       = False
all_puos = ["PUO_01"] if TEST_MODE else all_puos

# -----------------------------------------------------------------------------
# plot temporal coverage
# -----------------------------------------------------------------------------

if PLOT_TEMPORAL_COVERAGE:
    print("Plot temporal coverage...")
    plot_temporal_coverage()

# -----------------------------------------------------------------------------
# plot time series
# -----------------------------------------------------------------------------

if PLOT_TIME_SERIES:
    print("Plot time series...")
    for period in all_puos:
        for device in ["EXPE", "SONIC"]:
            print("\t", period, "&", device)
        
            _, _, start_datetime, end_datetime, date, _ = metadata(period)

            for var in variables[device]:
                plot_ts(
                    x=get_var(device, period, "Datetime"),
                    y=get_var(device, period, var),
                    fn=f"{period}_{device}_{var}", 
                    title = f"""{labels[var]}\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {SAMPLE_RATE[device]} Hz)"""
                    )

# -----------------------------------------------------------------------------
# plot spectrum data
# -----------------------------------------------------------------------------

if PLOT_SPECTRUM_DATA:
    print("Plot spectrum data...")
    for period in all_puos:
        _, _, start_datetime, end_datetime, date, _ = metadata(period)
        
        for device in ["EXPE", "SONIC"]:
            print("\t", period, "&", device)
            
            # plot spectrum
            for var in variables[device]:
                plot_spectrum(
                    x=get_var(device, period, "Datetime"),
                    y=get_var(device, period, var),
                    fn=f"{period}_{device}_{var}",
                    ylabel=labels[var], 
                    title = f"""{labels[var]}\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {SAMPLE_RATE[device]} Hz)"""
                    )
        
        # plot comparison normalized spectra
        plot_patterns(period)
    
    # plot comparison smoothed spectra
    plot_spectrum_comp("EXPE")
    plot_spectrum_comp("SONIC")
    plot_t_spectrum_comp()
    plot_wind_spectrum_comp()
    
    # plot spectra correlation matrix
    plot_mean_corr()

# -----------------------------------------------------------------------------
# plot window function influence
# -----------------------------------------------------------------------------

if PLOT_WINDOW_FUNCTION_INFLUENCE:
    print("Plot window function influence...")

    # plot window functions
    plot_win()

    # plot influence of window functions on spectra
    for period in all_puos:
        _, _, start_datetime, end_datetime, date, _ = metadata(period)
        
        for device in ["EXPE", "SONIC"]:
            print("\t", period, "&", device)
            
            for var in variables[device]:
                plot_win_influence(
                        x=get_var(device, period, "Datetime"),
                        y=get_var(device, period, var),
                        title=f"""{labels[var]}\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {SAMPLE_RATE[device]} Hz)""",
                        fn=f"wf_{period}_{device}_{var}"
                        )

# -----------------------------------------------------------------------------
# plot averaging
# -----------------------------------------------------------------------------

if PLOT_AVERAGING:
    print("Plot averaging...")
    error_metrics = pd.DataFrame()
    
    for period in all_puos:
        _, _, start_datetime, end_datetime, date, _ = metadata(period)
        
        for device in ["EXPE", "SONIC"]:
            print("\t", period, "&", device)



            for var in variables[device]:
                error_metrics_dict = plot_avg(
                    x=get_var(device, period, "Datetime"),
                    y=get_var(device, period, var),
                    device=device,
                    title=f"""{labels[var]}\n{date}: {start_datetime[10:-3]} - {end_datetime[10:-3]}\n({device}, {SAMPLE_RATE[device]} Hz)""",
                    fn=f"avg_{period}_{device}_{var}"
                    )
                
                error_metrics_dict["PUO"] = period
                error_metrics_dict["Device"] = device
                error_metrics_dict["Variable"] = var
                
                error_metrics = error_metrics.append(error_metrics_dict, ignore_index=True)
                
    error_metrics.to_csv("data/avg_error_metrics.csv", index=False)

    plot_error_metrics()

# -----------------------------------------------------------------------------
# plot turbulence intensity
# -----------------------------------------------------------------------------

if PLOT_TURBULENCE_INTENSITY:
    print("Plot turbulence intensity...")
    plot_turb_intensity(which="abs")
    plot_turb_intensity(which="rel")

# -----------------------------------------------------------------------------

print("Done!")

# print(f"\tTurbulente Intensität Horizontalwind: {turbulente_intensitaet(y=timeseries_data['wind_h'])}")
# print(f"\tTurbulente Intensität Vertikalwind {turbulente_intensitaet(y=timeseries_data['wind_z'])}")
