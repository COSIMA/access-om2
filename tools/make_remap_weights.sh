#!/bin/bash
#PBS -P x77
#PBS -q normal
#PBS -l ncpus=288,mem=512GB,walltime=05:00:00,jobfs=100GB
#PBS -l wd
#PBS -lstorage=scratch/v45+gdata/hh5+gdata/ik11+gdata/ua8

module purge
module load python3-as-python
module load nco
module use /g/data/hh5/public/modules
module load conda/analysis3
module unload openmpi
module load openmpi/4.0.2

# Make all 1 deg weights.
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_1deg/ --ocean MOM1 --npes 288 --atm JRA55
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_1deg/ --ocean MOM1 --npes 288 --atm ERA5

# Make all 0.25 deg weights.
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_025deg/ --ocean MOM025 --npes 288 --atm JRA55
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_025deg/ --ocean MOM025 --npes 288 --atm ERA5

# Make all 0.1 deg weights.
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_01deg/ --ocean MOM01 --npes 288 --atm JRA55
time ./make_remap_weights.py /g/data/ik11/inputs/access-om2/input_20201102 /g/data/ua8/JRA55-do/RYF/v1-3/ /g/data/ik11/inputs/access-om2/input_20201102/yatm_01deg/ --ocean MOM01 --npes 288 --atm ERA5
