#!/bin/bash

# Wybrane "rates"
rates=(50 100 200)

# Pętla przez wszystkie "rates"
for rate in "${rates[@]}"
do
    ~/.local/git/vegeta/vegeta attack -duration=15s -rate "$rate" -targets target.txt | vegeta report -type=text #encode -to csv
done
