#!/usr/bin/env sh

# Compile ACCESS-OM2 at 1, 1/4 and 1/10 degree resolution with JRA-55-do forcing
# Andrew Kiss https://github.com/aekiss

set -e

#Type of MOM installation

export mom_type=ACCESS-OM
#export mom_type=ACCESS-OM-BGC

echo "MOM5 build is of type mom_type=${mom_type}"
sleep 1

# Disable user gitconfig
export GIT_CONFIG_NOGLOBAL=yes

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    echo "Installing ACCESS-OM2 in $(pwd)"
    export ACCESS_OM_DIR=$(pwd)
fi
export LIBACCESSOM2_ROOT=$ACCESS_OM_DIR/src/libaccessom2

declare -a exepaths=(${ACCESS_OM_DIR}/src/mom/exec/nci/${mom_type}/fms_${mom_type}.x ${LIBACCESSOM2_ROOT}/build/bin/yatm.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_722p/cice_auscom_3600x2700_722p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_18x15.3600x2700_1682p/cice_auscom_18x15.3600x2700_1682p.exe ${ACCESS_OM_DIR}/src/mom/bin/mppnccombine.nci)
# ${ACCESS_OM_DIR}/src/matm/build_nt62/matm_nt62.exe
# ${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe

cd ${ACCESS_OM_DIR}

# echo "Downloading experiment input data and creating directories..."
# ${ACCESS_OM_DIR}/get_input_data.py

echo
echo "Removing previous executables (if any)..."
for p in "${exepaths[@]}"
do
    rm ${p} && echo "rm ${p}"
done

echo
echo "Compiling YATM file-based atmosphere and libaccessom2... "
cd ${LIBACCESSOM2_ROOT}
source ./build_on_gadi.sh

echo
echo "Compiling MOM5.1..."
cd ${ACCESS_OM_DIR}/src/mom/exp
./MOM_compile.csh --type $mom_type --platform nci

cd ${ACCESS_OM_DIR}/src/cice5
echo
echo "Compiling CICE5.1 at 1 degree..."
make # 1 degree
echo
echo "Compiling CICE5.1 at 1/4 degree..."
make 025deg
echo
echo "Compiling CICE5.1 at 1/10 degree..."
make 01deg
echo
echo "Compiling CICE5.1 at 1/10 degree with more blocks..."
make 01deg_18x15

echo
echo "Checking all executables have been built..."
for p in "${exepaths[@]}"
do
    ls ${p} || { echo "Build failed!"; exit 1; }
done

echo
source ${ACCESS_OM_DIR}/hashexe.sh

cd ${ACCESS_OM_DIR}
echo
echo "Executables were built using these library versions:"
source ${ACCESS_OM_DIR}/libcheck.sh

echo
echo "$(basename "$0") completed."
echo

# exit 0

