#!/usr/bin/env sh

# Make Fortran namelist of version info
# include this using #include version_info.nml
# Andrew Kiss https://github.com/aekiss

vnml=version_info.nml
rm -f $vnml || true  # because vnml is untracked and would otherwise set modified='.true.'
hash=`git rev-parse HEAD`
# modified=[-n "$(git status --porcelain)"]
modified='.false.'
test -z "$(git status --porcelain)" || modified='.true.' # uncommitted changes or untracked files
timestamp="$(date +%c)"
echo "&version_info_nml" >| $vnml
echo "    hash = '$hash'" >> $vnml
echo "    modified = $modified" >> $vnml
echo "    timestamp = '$timestamp'" >> $vnml
echo "    user = '$USER'" >> $vnml
echo "    hostname = '$HOSTNAME'" >> $vnml
echo "    use_this_module = .true." >> $vnml
echo "/" >> $vnml
