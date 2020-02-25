#!/usr/bin/env sh

# Pull latest sources from master in all submodules, recompile,
# copy updated exes to public dir, update config.yaml, 
# commit and push submodule changes.
#
# Andrew Kiss https://github.com/aekiss

set -e

export public=/g/data/ik11/inputs/access-om2/bin  # also used in hashexe-public.sh
if [ -w $public ]; then
    bindir=$public                                                           
else
    echo "You don't have write access to $public. Perhaps you should use update-all.sh instead? Exiting."
    exit 1
fi

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    echo "Installing ACCESS-OM2 in $(pwd)"
    export ACCESS_OM_DIR=$(pwd)
fi

source ${ACCESS_OM_DIR}/update-all.sh

source ${ACCESS_OM_DIR}/hashexe-public.sh && { cd ${ACCESS_OM_DIR}; git submodule foreach 'git commit -am "Update to latest model executables" && { echo "Committed updated config.yaml; now pushing"; git push; }; echo ' ; }

echo "Completed."
