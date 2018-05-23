#!/usr/bin/env sh

# Copy ACCESS-OM2 JRA55 executables to bin with githash in name, and config.yaml to match.
# All changes to config.yaml are reported.
# Andrew Kiss https://github.com/aekiss

set -e

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    export ACCESS_OM_DIR=$(pwd)
fi

matmcorepath=${ACCESS_OM_DIR}/src/matm/build_nt62/matm_nt62.exe
matmpath=${ACCESS_OM_DIR}/src/matm/build_jra55/matm_jra55.exe
fmspath=${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
cice1path=${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
cice025path=${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
# cice010path=${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1200p/cice_auscom_3600x2700_1200p.exe
# cice010path=${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_2700p/cice_auscom_3600x2700_2700p.exe
# cice010path=${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1440p/cice_auscom_3600x2700_1440p.exe
cice010path=${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_2000p/cice_auscom_3600x2700_2000p.exe
mppnccombinepath=${ACCESS_OM_DIR}/src/mom/bin/mppnccombine.nci

config1corepath=${ACCESS_OM_DIR}/control/1deg_core_nyf/config.yaml
config1path=${ACCESS_OM_DIR}/control/1deg_jra55_ryf/config.yaml
config025path=${ACCESS_OM_DIR}/control/025deg_jra55_ryf/config.yaml
config010path=${ACCESS_OM_DIR}/control/01deg_jra55_ryf/config.yaml

bindir=${ACCESS_OM_DIR}/bin

mkdir -p ${bindir}

echo "Getting executable hashes..."

cd $(dirname "${matmpath}") && matmhash=`git rev-parse --short=8 HEAD` # NB same matm hash for core and jra55
cd $(dirname "${fmspath}") && fmshash=`git rev-parse --short=8 HEAD`
cd $(dirname "${cice1path}") && cicehash=`git rev-parse --short=8 HEAD` # NB only one hash for all three cice builds

echo "Copying executables to "${bindir}" with hashes added to names..."

matmcorebn=$(basename "${matmcorepath}")
matmcorehashexe="${matmcorebn%.*}"_${matmhash}."${matmcorepath##*.}"
echo "  cp ${matmcorepath} ${bindir}/${matmcorehashexe}"
        cp ${matmcorepath} ${bindir}/${matmcorehashexe}

matmbn=$(basename "${matmpath}")
matmhashexe="${matmbn%.*}"_${matmhash}."${matmpath##*.}"
echo "  cp ${matmpath} ${bindir}/${matmhashexe}"
        cp ${matmpath} ${bindir}/${matmhashexe}

fmsbn=$(basename "${fmspath}")
fmshashexe="${fmsbn%.*}"_${fmshash}."${fmspath##*.}"
echo "  cp ${fmspath} ${bindir}/${fmshashexe}"
        cp ${fmspath} ${bindir}/${fmshashexe}

cice1bn=$(basename "${cice1path}")
cice1hashexe="${cice1bn%.*}"_${cicehash}."${cice1path##*.}"
echo "  cp ${cice1path} ${bindir}/${cice1hashexe}"
        cp ${cice1path} ${bindir}/${cice1hashexe}

cice025bn=$(basename "${cice025path}")
cice025hashexe="${cice025bn%.*}"_${cicehash}."${cice025path##*.}"
echo "  cp ${cice025path} ${bindir}/${cice025hashexe}"
        cp ${cice025path} ${bindir}/${cice025hashexe}

cice010bn=$(basename "${cice010path}")
cice010hashexe="${cice010bn%.*}"_${cicehash}."${cice010path##*.}"
echo "  cp ${cice010path} ${bindir}/${cice010hashexe}"
        cp ${cice010path} ${bindir}/${cice010hashexe}

echo "  cp ${mppnccombinepath} ${bindir}/mppnccombine"
		cp ${mppnccombinepath} ${bindir}/mppnccombine # no hash for mppnccombine


echo "Fixing exe in "${config1corepath}" to match executable names..."
sed "s/${matmcorebn%.*}.*/${matmcorehashexe}/g" < ${config1corepath} > ${config1corepath}-tmp
sed "s/${fmsbn%.*}.*/${fmshashexe}/g" < ${config1corepath}-tmp > ${config1corepath}-tmp2
sed "s/${cice1bn%.*}.*/${cice1hashexe}/g" < ${config1corepath}-tmp2 > ${config1corepath}-tmp3
diff ${config1corepath} ${config1corepath}-tmp3 || true
mv ${config1corepath}-tmp3 ${config1corepath}
rm ${config1corepath}-tmp*

echo "Fixing exe in "${config1path}" to match executable names..."
sed "s/${matmbn%.*}.*/${matmhashexe}/g" < ${config1path} > ${config1path}-tmp
sed "s/${fmsbn%.*}.*/${fmshashexe}/g" < ${config1path}-tmp > ${config1path}-tmp2
sed "s/${cice1bn%.*}.*/${cice1hashexe}/g" < ${config1path}-tmp2 > ${config1path}-tmp3
diff ${config1path} ${config1path}-tmp3 || true
mv ${config1path}-tmp3 ${config1path}
rm ${config1path}-tmp*

echo "Fixing exe in "${config025path}" to match executable names..."
sed "s/${matmbn%.*}.*/${matmhashexe}/g" < ${config025path} > ${config025path}-tmp
sed "s/${fmsbn%.*}.*/${fmshashexe}/g" < ${config025path}-tmp > ${config025path}-tmp2
sed "s/${cice025bn%.*}.*/${cice025hashexe}/g" < ${config025path}-tmp2 > ${config025path}-tmp3
diff ${config025path} ${config025path}-tmp3 || true
mv ${config025path}-tmp3 ${config025path}
rm ${config025path}-tmp*

echo "Fixing exe in "${config010path}" to match executable names..."
sed "s/${matmbn%.*}.*/${matmhashexe}/g" < ${config010path} > ${config010path}-tmp
sed "s/${fmsbn%.*}.*/${fmshashexe}/g" < ${config010path}-tmp > ${config010path}-tmp2
sed "s/${cice010bn%.*}.*/${cice010hashexe}/g" < ${config010path}-tmp2 > ${config010path}-tmp3
diff ${config010path} ${config010path}-tmp3 || true
mv ${config010path}-tmp3 ${config010path}
rm ${config010path}-tmp*

echo "$(basename $BASH_SOURCE) completed."

