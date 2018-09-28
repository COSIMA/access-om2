#!/usr/bin/env sh

# Copy ACCESS-OM2 executables to bin with githash in name, and config.yaml to match.
# All changes to config.yaml are reported.
# Andrew Kiss https://github.com/aekiss

set -e

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    export ACCESS_OM_DIR=$(pwd)
fi

yatmpath=${ACCESS_OM_DIR}/src/libaccessom2/build/bin/yatm.exe
fmspath=${ACCESS_OM_DIR}/src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x
cice1path=${ACCESS_OM_DIR}/src/cice5/build_auscom_360x300_24p/cice_auscom_360x300_24p.exe
cice025path=${ACCESS_OM_DIR}/src/cice5/build_auscom_1440x1080_480p/cice_auscom_1440x1080_480p.exe
cice010path=${ACCESS_OM_DIR}/src/cice5/build_auscom_3600x2700_1392p/cice_auscom_3600x2700_1392p.exe
mppnccombinepath=${ACCESS_OM_DIR}/src/mom/bin/mppnccombine.nci

config1corepath=${ACCESS_OM_DIR}/control/1deg_core_nyf/config.yaml  # TODO: do this

config1ryfpath=${ACCESS_OM_DIR}/control/1deg_jra55_ryf/config.yaml
config025ryfpath=${ACCESS_OM_DIR}/control/025deg_jra55_ryf/config.yaml
config010ryfpath=${ACCESS_OM_DIR}/control/01deg_jra55_ryf/config.yaml

config1iafpath=${ACCESS_OM_DIR}/control/1deg_jra55_iaf/config.yaml
config025iafpath=${ACCESS_OM_DIR}/control/025deg_jra55_iaf/config.yaml
config010iafpath=${ACCESS_OM_DIR}/control/01deg_jra55_iaf/config.yaml

bindir=${ACCESS_OM_DIR}/bin

mkdir -p ${bindir}

echo "Getting executable hashes..."

cd $(dirname "${yatmpath}") && yatmhash=`git rev-parse --short=7 HEAD`
test -z "$(git status --porcelain)" || yatmhash=${yatmhash}-modified # uncommitted changes or untracked files
cd $(dirname "${fmspath}") && fmshash=`git rev-parse --short=7 HEAD`
test -z "$(git status --porcelain)" || fmshash=${fmshash}-modified # uncommitted changes or untracked files
fmshash=${fmshash}_libaccessom2_${yatmhash} # also track libaccessom2
cd $(dirname "${cice1path}") && cicehash=`git rev-parse --short=7 HEAD` # NB only one hash for all three cice builds
test -z "$(git status --porcelain)" || cicehash=${cicehash}-modified # uncommitted changes or untracked files
cicehash=${cicehash}_libaccessom2_${yatmhash} # also track libaccessom2

echo "Copying executables to "${bindir}" with hashes added to names..."

yatmbn=$(basename "${yatmpath}")
yatmhashexe="${yatmbn%.*}"_${yatmhash}."${yatmpath##*.}"
echo "  cp ${yatmpath} ${bindir}/${yatmhashexe}"
        cp ${yatmpath} ${bindir}/${yatmhashexe}

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


echo "Fixing exe in "${config1ryfpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config1ryfpath} > ${config1ryfpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config1ryfpath}-tmp > ${config1ryfpath}-tmp2
sed "s|exe:.*${cice1bn%.*}_.*|exe: ${bindir}/${cice1hashexe}|g" < ${config1ryfpath}-tmp2 > ${config1ryfpath}-tmp3
diff ${config1ryfpath} ${config1ryfpath}-tmp3 || true
mv ${config1ryfpath}-tmp3 ${config1ryfpath}
rm ${config1ryfpath}-tmp*

echo "Fixing exe in "${config025ryfpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config025ryfpath} > ${config025ryfpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config025ryfpath}-tmp > ${config025ryfpath}-tmp2
sed "s|exe:.*${cice025bn%.*}_.*|exe: ${bindir}/${cice025hashexe}|g" < ${config025ryfpath}-tmp2 > ${config025ryfpath}-tmp3
diff ${config025ryfpath} ${config025ryfpath}-tmp3 || true
mv ${config025ryfpath}-tmp3 ${config025ryfpath}
rm ${config025ryfpath}-tmp*

echo "Fixing exe in "${config010ryfpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config010ryfpath} > ${config010ryfpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config010ryfpath}-tmp > ${config010ryfpath}-tmp2
sed "s|exe:.*${cice010bn%.*}_.*|exe: ${bindir}/${cice010hashexe}|g" < ${config010ryfpath}-tmp2 > ${config010ryfpath}-tmp3
diff ${config010ryfpath} ${config010ryfpath}-tmp3 || true
mv ${config010ryfpath}-tmp3 ${config010ryfpath}
rm ${config010ryfpath}-tmp*


echo "Fixing exe in "${config1iafpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config1iafpath} > ${config1iafpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config1iafpath}-tmp > ${config1iafpath}-tmp2
sed "s|exe:.*${cice1bn%.*}_.*|exe: ${bindir}/${cice1hashexe}|g" < ${config1iafpath}-tmp2 > ${config1iafpath}-tmp3
diff ${config1iafpath} ${config1iafpath}-tmp3 || true
mv ${config1iafpath}-tmp3 ${config1iafpath}
rm ${config1iafpath}-tmp*

echo "Fixing exe in "${config025iafpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config025iafpath} > ${config025iafpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config025iafpath}-tmp > ${config025iafpath}-tmp2
sed "s|exe:.*${cice025bn%.*}_.*|exe: ${bindir}/${cice025hashexe}|g" < ${config025iafpath}-tmp2 > ${config025iafpath}-tmp3
diff ${config025iafpath} ${config025iafpath}-tmp3 || true
mv ${config025iafpath}-tmp3 ${config025iafpath}
rm ${config025iafpath}-tmp*

echo "Fixing exe in "${config010iafpath}" to match executable names..."
sed "s|exe:.*${yatmbn%.*}_.*|exe: ${bindir}/${yatmhashexe}|g" < ${config010iafpath} > ${config010iafpath}-tmp
sed "s|exe:.*${fmsbn%.*}_.*|exe: ${bindir}/${fmshashexe}|g" < ${config010iafpath}-tmp > ${config010iafpath}-tmp2
sed "s|exe:.*${cice010bn%.*}_.*|exe: ${bindir}/${cice010hashexe}|g" < ${config010iafpath}-tmp2 > ${config010iafpath}-tmp3
diff ${config010iafpath} ${config010iafpath}-tmp3 || true
mv ${config010iafpath}-tmp3 ${config010iafpath}
rm ${config010iafpath}-tmp*


echo "$(basename $BASH_SOURCE) completed."

