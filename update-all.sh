#!/usr/bin/env sh

# Update all submodules to latest remote commits on master, recompile, and update exe in all config.yaml
#
# Andrew Kiss https://github.com/aekiss

set -e

if [[ -z "${ACCESS_OM_DIR}" ]]; then
    echo "Installing ACCESS-OM2 in $(pwd)"
    export ACCESS_OM_DIR=$(pwd)
fi

source ${ACCESS_OM_DIR}/update-submodules.sh
source ${ACCESS_OM_DIR}/install.sh

echo "$(basename $BASH_SOURCE) completed."
