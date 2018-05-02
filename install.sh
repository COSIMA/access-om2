#!/usr/bin/env sh

# Compile ACCESS-OM2 at 1, 1/4 and 1/10 degree resolution wth JRA-55 forcing
# NB: requires ACCESS_OM_DIR environment variable.
# Andrew Kiss https://github.com/aekiss

set -e

export LIBACCESSOM2_ROOT=$ACCESS_OM_DIR/src/libaccessom2

cd ${ACCESS_OM_DIR}

# echo "Downloading experiment input data and creating directories..."
# ./get_input_data.py

echo "Compiling YATM file-based atmosphere and libaccessom2... "

mkdir -p ${LIBACCESSOM2_ROOT}/build
cd ${LIBACCESSOM2_ROOT}/build

module purge
module load cmake/3.6.2
module load netcdf/4.4.1.1
module load intel-fc/17.0.1.132
module load openmpi/1.10.2
cmake ../
make

echo "Compiling MOM5.1..."
rm -f $ACCESS_OM_DIR/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
cd ${ACCESS_OM_DIR}/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci

echo "Compiling CICE5.1 at 1 degree..."
rm -f $ACCESS_OM_DIR/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
rm -f $ACCESS_OM_DIR/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
rm -f $ACCESS_OM_DIR/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe

cd ${ACCESS_OM_DIR}/src/cice5
make # 1 degree
echo "Compiling CICE5.1 at 1/4 degree..."
make 025deg
echo "Compiling CICE5.1 at 1/10 degree..."
make 01deg

echo "Checking all executables have been built..."
ls ${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
ls ${LIBACCESSOM2_ROOT}/build/bin/yatm.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe

source ${ACCESS_OM_DIR}/hashexe.sh

echo "Success."
echo "You will need to edit project, shortpath and possibly timestep in ${ACCESS_OM_DIR}/control/*/config.yaml"

exit 0

