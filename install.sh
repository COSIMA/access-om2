#!/usr/bin/env sh

# Compile ACCESS-OM2 at 1, 1/4 and 1/10 degree resolution wth JRA-55 forcing
# Andrew Kiss https://github.com/aekiss

set -e

# Disable user gitconfig
export GIT_CONFIG_NOGLOBAL=yes

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    echo "Installing ACCESS-OM2 in $(pwd)"
    export ACCESS_OM_DIR=$(pwd)
fi
export LIBACCESSOM2_ROOT=$ACCESS_OM_DIR/src/libaccessom2

declare -a exepaths=(${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x ${LIBACCESSOM2_ROOT}/build/bin/yatm.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_432p/cice_auscom_3600x2700_432p.exe)
# ${ACCESS_OM_DIR}/src/matm/build_nt62/matm_nt62.exe
# ${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe

cd ${ACCESS_OM_DIR}

# echo "Downloading experiment input data and creating directories..."
# ${ACCESS_OM_DIR}/get_input_data.py

echo "Removing previous executables (if any)..."
for p in "${exepaths[@]}"
do
    rm ${p} && echo "rm ${p}"
done

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
cd ${ACCESS_OM_DIR}/src/mom/exp
./MOM_compile.csh --type ACCESS-OM --platform nci

cd ${ACCESS_OM_DIR}/src/cice5
echo "Compiling CICE5.1 at 1 degree..."
make # 1 degree
echo "Compiling CICE5.1 at 1/4 degree..."
make 025deg
echo "Compiling CICE5.1 at 1/10 degree..."
make 01deg

echo "Checking all executables have been built..."
for p in "${exepaths[@]}"
do
    ls ${p} || { echo "Build failed!"; exit 1; }
done

source ${ACCESS_OM_DIR}/hashexe.sh

cd ${ACCESS_OM_DIR}
echo "Executables were built using these library versions:"
source ${ACCESS_OM_DIR}/libcheck.sh

echo
echo "$(basename "$0") completed."
echo
echo "You will need to edit project, shortpath and possibly timestep in" 
ls -1 ${ACCESS_OM_DIR}/control/*/config.yaml

exit 0

