#!/usr/bin/env sh

# Compile ACCESS-OM2 at 1, 1/4 and 1/10 degree resolution wth JRA-55 forcing
# NB: requires ACCESS_OM_DIR environment variable.
# Andrew Kiss https://github.com/aekiss

set -e

export OASIS_ROOT=${ACCESS_OM_DIR}/src/oasis3-mct/

cd ${ACCESS_OM_DIR}

# echo "Downloading experiment input data and creating directories..."
# ./get_input_data.py

echo "Compiling OASIS3-MCT..."
cd ${OASIS_ROOT}
make

echo "Compiling MOM5.1..."
cd ${ACCESS_OM_DIR}/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci

echo "Compiling CICE5.1 at 1 degree..."
cd ${ACCESS_OM_DIR}/src/cice5
make # 1 degree
echo "Compiling CICE5.1 at 1/4 degree..."
make 025deg
echo "Compiling CICE5.1 at 1/10 degree..."
make 01deg

echo "Compiling MATM JRA-55 file-based atmosphere... "
cd ${ACCESS_OM_DIR}/src/matm
make jra55

echo "Checking all executables have been built..."
ls ${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
ls ${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
ls ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe

source ${ACCESS_OM_DIR}/hashexe.sh

echo "Success."
echo "You will need to edit project, shortpath and possibly timestep in ${ACCESS_OM_DIR}/control/*/config.yaml"

exit 0

