#!/usr/bin/env sh

# Compile ACCESS-OM2 at 1, 1/4 and 1/10 degree resolution wth JRA-55 forcing
# and with CORE forcing at 1 degree resolution.
# Andrew Kiss https://github.com/aekiss

set -e

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    echo "Installing ACCESS-OM2 in $(pwd)"
    export ACCESS_OM_DIR=$(pwd)
fi
export OASIS_ROOT=${ACCESS_OM_DIR}/src/oasis3-mct/

declare -a exepaths=(${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x ${ACCESS_OM_DIR}/src/matm/build_nt62/matm_nt62.exe ${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_2000p/cice_auscom_3600x2700_2000p.exe)
# ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe)
# ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_2700p/cice_auscom_3600x2700_2700p.exe)
# ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1440p/cice_auscom_3600x2700_1440p.exe)

cd ${ACCESS_OM_DIR}

echo "Downloading experiment input data and creating directories..."
${ACCESS_OM_DIR}/get_input_data.py

echo "Removing previous executables (if any)..."
for p in "${exepaths[@]}"
do
    rm ${p} && echo "rm ${p}"
done

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

echo "Compiling MATM CORE file-based atmosphere... "
cd ${ACCESS_OM_DIR}/src/matm
make core

echo "Compiling MATM JRA-55 file-based atmosphere... "
cd ${ACCESS_OM_DIR}/src/matm
make jra55

echo "Checking all executables have been built..."
for p in "${exepaths[@]}"
do
    ls ${p}
done

source ${ACCESS_OM_DIR}/hashexe.sh

cd ${ACCESS_OM_DIR}
echo "Executables were built using these library versions:"
source ${ACCESS_OM_DIR}/libcheck.sh

echo "$(basename $BASH_SOURCE) completed."
echo "You will need to edit project, shortpath and possibly timestep in ${ACCESS_OM_DIR}/control/*/config.yaml"

exit 0

