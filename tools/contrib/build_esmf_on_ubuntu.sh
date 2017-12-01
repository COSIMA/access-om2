#!/bin/bash

mkdir bin
sudo apt-get install libnetcdf-dev libnetcdff-dev
wget http://s3-ap-southeast-2.amazonaws.com/dp-drop/ocean-regrid/contrib/esmf_7_0_0_src.tar.gz
tar zxvf esmf_7_0_0_src.tar.gz
cd esmf
export ESMF_DIR=$(pwd)
export ESMF_NETCDF="split"
export ESMF_NETCDF_INCLUDE=/usr/include/
export ESMF_NETCDF_LIBPATH=/usr/lib/x86_64-linux-gnu/
export ESMF_NETCDF_LIBS="-lnetcdff -lnetcdf"
make
cd src/apps/ESMF_RegridWeightGen
make
cd ../../../../
cp esmf/apps/appsO/*/ESMF_RegridWeightGen bin/
export PATH=$(pwd)/bin:$PATH
