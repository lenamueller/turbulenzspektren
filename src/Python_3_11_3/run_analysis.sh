#!/bin/bash

echo "Run analysis..."

for measuring_situation in "ES_2023_07_08_morning" "ES_2023_07_08_noon" "ES_2023_07_08_afternoon" "ES_2023_07_11_morning" "GAS_2023_07_11_noon" "ES_2023_07_11_noon"
do
    python fft.py $measuring_situation "EXPE"
    python fft.py $measuring_situation "SONIC"
    python averaging.py $measuring_situation "EXPE"
    python averaging.py $measuring_situation "SONIC"
done

echo "Done"
