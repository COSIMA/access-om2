#!/bin/bash
#PBS -P x77
#PBS -q normal
#PBS -l ncpus=256,mem=512,walltime=05:00:00,jobfs=100GB
#PBS -l wd

module load esmf/6.3.0rp1-intel

time ./make_remap_weights.py /short/x77/nah599/access-om2/input/ /g/data1/ua8/JRA55-do/RYF/v1-3/  --ocean MOM01 --npes 256
