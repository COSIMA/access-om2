#!/bin/bash
set -x
set -e

git archive --remote=git://git.code.sf.net/p/esmf/esmf --format=tar --prefix=esmf/ ESMF_7_1_0r | tar xf -
#module load netcdf/4.7.4
module load netcdf/4.6.3
#module load intel-compiler/2020.2.254
module load intel-compiler/2019.3.199
#module load gcc
mkdir -p bin
cd esmf
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
cp esmf/apps/appsO/*/ESMF_RegridWeightGen bin/
export PATH=$(pwd)/bin:$PATH
