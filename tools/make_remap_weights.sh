#!/bin/bash
#PBS -P x77
#PBS -q normal
#PBS -l ncpus=288,mem=512GB,walltime=05:00:00,jobfs=100GB
#PBS -l wd
#PBS -lstorage=scratch/v45+gdata/hh5+gdata/ik11+gdata/ua8+gdata/rt52

module purge
module load python3-as-python
module load nco
module use /g/data/hh5/public/modules
module load conda/analysis3
module unload openmpi
module load openmpi/4.0.2

# Make all 1 deg weights.
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/ua8/JRA55-do/RYF/v1-3/RYF.t_10.1990_1991.nc --ocean MOM1 --npes 288 --atm JRA55
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/rt52/era5/single-levels/reanalysis/2t/1980/2t_era5_oper_sfc_19800101-19800131.nc --ocean MOM1 --npes 288 --atm ERA5

# Make all 0.25 deg weights.
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/ua8/JRA55-do/RYF/v1-3/RYF.t_10.1990_1991.nc --ocean MOM025 --npes 288 --atm JRA55
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/rt52/era5/single-levels/reanalysis/2t/1980/2t_era5_oper_sfc_19800101-19800131.nc --ocean MOM025 --npes 288 --atm ERA5

# Make all 0.1 deg weights.
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/ua8/JRA55-do/RYF/v1-3/RYF.t_10.1990_1991.nc --ocean MOM01 --npes 288 --atm JRA55
time ./make_remap_weights.py --accessom2_input_dir /g/data/ik11/inputs/access-om2/input_20201102 --atm_forcing_file /g/data/rt52/era5/single-levels/reanalysis/2t/1980/2t_era5_oper_sfc_19800101-19800131.nc --ocean MOM01 --npes 288 --atm ERA5
