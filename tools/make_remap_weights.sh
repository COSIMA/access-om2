#!/bin/bash
#PBS -P x77
#PBS -q normal
#PBS -l ncpus=256,mem=512,walltime=05:00:00,jobfs=100GB
#PBS -l wd

module load esmf/7.1.0r-intel

# Make all 0.1 deg weights.
time ./make_remap_weights.py /short/x77/nah599/access-om2/input/ /g/data1/ua8/JRA55-do/RYF/v1-3/ /short/x77/nah599/access-om2/input/yatm_1deg/ --ocean MOM01 --npes 256
