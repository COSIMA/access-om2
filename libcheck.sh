#!/usr/bin/env sh

# Report library versions used in model components
# Andrew Kiss https://github.com/aekiss

declare -a libs=(openmpi netcdf)
declare -a paths=(src/cice5/bld/config.nci.auscom.360x300 src/cice5/bld/config.nci.auscom.3600x2700 src/cice5/bld/config.nci.auscom.1440x1080 src/matm/build/environs.nci src/mom/bin/environs.nci src/oasis3-mct/util/make_dir/config.nci)
for l in "${libs[@]}"
do
    echo $l library versions used:
    for p in "${paths[@]}"
    do
        grep -H $l $p
    done
done
echo "Installing ACCESS-OM2 in $(pwd)"

exit 0
