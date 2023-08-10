#!/bin/bash

echo "Run analysis..."
for measuring_situation in "ES_2023_07_08" "ES_2023_07_11" "GAS_2023_07_11"
do
    python fft.py $measuring_situation "EXPE"
    python fft.py $measuring_situation "SONIC"
done

for measuring_situation in "ES_2023_07_08" "ES_2023_07_11" "GAS_2023_07_11"
do
    python averaging.py $measuring_situation "EXPE"
    python averaging.py $measuring_situation "SONIC"
done
echo "Done"
