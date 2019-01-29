#!/usr/bin/env sh

# Report library versions used in model components of ACCESS-OM2
# Andrew Kiss https://github.com/aekiss

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    export ACCESS_OM_DIR=$(pwd)
fi
if [[ -z "${LIBACCESSOM2_ROOT}" ]]; then
    export LIBACCESSOM2_ROOT=$ACCESS_OM_DIR/src/libaccessom2
fi
# if [[ -z "${OASIS_ROOT}" ]]; then
#     export OASIS_ROOT=${ACCESS_OM_DIR}/src/oasis3-mct
# fi

declare -a libs=(openmpi netcdf)
declare -a paths=(${ACCESS_OM_DIR}/src/mom/bin/environs.nci ${ACCESS_OM_DIR}/src/cice5/bld/config.nci.auscom.360x300 ${ACCESS_OM_DIR}/src/cice5/bld/config.nci.auscom.1440x1080 ${ACCESS_OM_DIR}/src/cice5/bld/config.nci.auscom.3600x2700 ${LIBACCESSOM2_ROOT}/build_on_raijin.sh)
 # ${OASIS_ROOT}/util/make_dir/config.nci)
# ${ACCESS_OM_DIR}/src/matm/build/environs.nci
declare -a exepaths=(${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x ${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe ${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_432p/cice_auscom_3600x2700_432p.exe ${LIBACCESSOM2_ROOT}/build/bin/yatm.exe)
# ${ACCESS_OM_DIR}/src/matm/build_nt62/matm_nt62.exe ${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe 
for l in "${libs[@]}"
do
    echo $l library versions used:
    echo "   in build scripts:"
    for p in "${paths[@]}"
    do
        echo -n "      "
        grep -H $l $p
    done
    echo "   in executables:"
    for p in "${exepaths[@]}"
    do
        echo "      $p: "
        ldd $p | grep $l
    done
done
