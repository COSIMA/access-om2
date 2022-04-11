#!/bin/bash
set -x
set -e

# use Russ' fixed code - see https://github.com/COSIMA/access-om2/issues/216
git clone https://github.com/COSIMA/esmf.git || true
cd esmf
git checkout f536c3e12d501e2ee1d4caf95cb425f5be6e84d3

#module load netcdf/4.7.4
module load netcdf/4.6.3
#module load intel-compiler/2020.2.254
module load intel-compiler/2019.3.199
#module load gcc
export ESMF_DIR=$(pwd)
export ESMF_F90COMPILER=ifort
export ESMF_F90LINKER=ifort
export ESMF_NETCDF=nc-config
#export ESMF_NETCDF="split"
export ESMF_NETCDF_INCLUDE=$NETCDF_ROOT/include
export ESMF_NETCDF_LIBPATH=$NETCDF_ROOT/lib
export ESMF_NETCDF_LIBS="-lnetcdff -lnetcdf"
make clean
make
cd src/apps/ESMF_RegridWeightGen
make
cd ../../../../
mkdir -p bin
cp esmf/apps/appsO/*/ESMF_RegridWeightGen bin/ESMF_RegridWeightGen_f536c3e12d
export PATH=$(pwd)/bin:$PATH
