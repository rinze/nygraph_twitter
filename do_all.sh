#!/bin/bash

for user in *.csv.gz; do 
    pngname=$(basename $user .csv.gz).png 
    test -e $pngname || (echo "Generating $pngname" && Rscript plot_data.R $user) 
done
