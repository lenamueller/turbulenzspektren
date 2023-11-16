

from setup import all_puos
from plot.plot_temporal_coverage import plot_temporal_coverage
from plot.plot_spectrum import plot_spectrum
from plot.plot_averaging import plot_averaging
from plot.plot_comparison import plot_comparison
from save_spectrum import save_spectrum


print("Run analysis...")

for puo in all_puos:
    
    for measuring_device in ["SONIC", "EXPE"]:
        
        print(f"-> PUO: {puo}, measuring devive: {measuring_device}")
        
        print("\tPlotting turbulence spectra")
        plot_spectrum(puo, measuring_device)
        
        print("\tSaving spectrum data for")
        save_spectrum(puo, measuring_device)
        
        print("\tPlotting averaging for")
        plot_averaging(puo, measuring_device)

print("\tPlotting temporal coverage")
plot_temporal_coverage()

print("\tPlotting comparison of all PUOs")
plot_comparison()

print("Analysis done.")