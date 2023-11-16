""" 
File: main.py
Author: Lena Müller
Date: November 16, 2023

Description: Main file for running the analysis.
"""

from setup import all_puos
from Datasets import ExpeDataset, SonicDataset
from plot.plot_temporal_coverage import plot_temporal_coverage
from plot.plot_spectrum import plot_spectrum
from plot.plot_averaging import plot_averaging
from plot.plot_comparison import plot_comparison
from plot.plot_influence_windows import plot_influence_windows, plot_windows


print("Run analysis...")

print("\tPlotting temporal coverage")
plot_temporal_coverage()

print("\tPlotting comparison of all PUOs")
plot_comparison()

print("Plotting window functions")
plot_windows()

for puo in all_puos:
    print("-> PUO", puo)

    # Create datasets
    ds_expe = ExpeDataset(puo)    
    ds_sonic = SonicDataset(puo)

    # Save spectrum data to csv-files
    ds_expe.save_spectrum_data(fn=f"data/spectra_data/{puo}_EXPE_spectrum_data.csv")
    ds_sonic.save_spectrum_data(fn=f"data/spectra_data/{puo}_SONIC_spectrum_data.csv")

    # Plot spectrum
    plot_spectrum(ds_expe)
    plot_spectrum(ds_sonic)
    
    # Plot averaging
    plot_averaging(ds_expe, type="rolling_mean")
    plot_averaging(ds_expe, type="fixed_intervalls")
    plot_averaging(ds_sonic, type="rolling_mean")
    plot_averaging(ds_sonic, type="fixed_intervalls")
    
    # # Plot sensitivity analysis
    plot_influence_windows(ds_sonic)

print("Analysis done.")