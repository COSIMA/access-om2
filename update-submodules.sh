#!/usr/bin/env sh

# Update all submodules to latest remote commits on master
# Andrew Kiss https://github.com/aekiss

set -e
git submodule foreach "git checkout master; git pull; echo"
echo "$(basename $BASH_SOURCE) completed."

