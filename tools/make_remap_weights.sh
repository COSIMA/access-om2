#!/bin/bash
#PBS -P x77
#PBS -q normal
#PBS -l ncpus=128,mem=496GB,walltime=02:00:00,jobfs=100GB
#PBS -l wd

time ./make_remap_weights.py /short/x77/nah599/access-om2/input/ /g/data1/ua8/JRA55-do/RYF/v1-3/  --npes 128

