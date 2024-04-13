#!/bin/bash


# Wybrane "rates"
rates=(50 100 200)

# Pętla przez wszystkie "rates"
for rate in "${rates[@]}"
do
    vegeta attack -duration=15s -rate "$rate" -targets target.txt |
    vegeta encode -to csv
done
