#!/bin/bash

echo "Run analysis..."

# plot raw data with temporal coverage
python plot_temporal_coverage.py


for puo in "PUO_00_0" "PUO_00_1" "PUO_01" "PUO_02" "PUO_03" "PUO_04" "PUO_05" "PUO_06" "PUO_07" "PUO_08"
do
    echo "PUO: $puo"

    # plot turbulence spectrum
    python plot_spectrum.py $puo "EXPE"
    python plot_spectrum.py $puo "SONIC"

    # plot averaging
    python plot_averaging.py $puo "EXPE"
    python plot_averaging.py $puo "SONIC"
done

echo "Done"