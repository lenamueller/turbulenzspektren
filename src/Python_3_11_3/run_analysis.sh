#!/bin/bash

echo "Run analysis..."

for puo in "PUO_00_0" "PUO_00_1" "PUO_01" "PUO_02" "PUO_03" "PUO_04" "PUO_05" "PUO_06" "PUO_07"
do
    python fft.py $puo "EXPE"
    python fft.py $puo "SONIC"
    python averaging.py $puo "EXPE"
    python averaging.py $puo "SONIC"
done

echo "Done"