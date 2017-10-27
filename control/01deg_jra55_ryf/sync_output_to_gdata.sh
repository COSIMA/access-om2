#!/bin/bash
#PBS -q copyq
#PBS -l ncpus=1
#PBS -l wd
#PBS -l walltime=1:00:00,mem=2GB
#PBS -P v45
#PBS -N sync_to_gdata

# Set this directory to something in /g/data3/hh5/tmp/cosima/
# (make a unique path for your set of runs)
GDATADIR=/ERROR/SET/GDATADIR/IN/sync_output_to_gdata.sh

mkdir -p ${GDATADIR}
cd archive
rsync --exclude "*.nc.*" -av --safe-links --no-g output* ${GDATADIR}
