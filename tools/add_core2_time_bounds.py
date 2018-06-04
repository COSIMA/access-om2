#!/usr/bin/env python

from __future__ import print_function

"""
The CORE2 forcing files have an ambiguous time dimension. For example in
ncar_precip.0001.nc:

TIME:units = "days since 1900-01-01 00:00:00" ;
TIME = 15.5, 45, 74.5, 105, 135.5, 166, 196.5, 227.5, 258, 288.5, 319, 349.5 ;

For a human this probably means that each time point refers to a month, however
for a computer that is trying to index on the basis of a date and time it is
ambiguous. For example which time point should be used for Jan 31? If an
algorithm tries to find the 'closest' time point it will choose the second one,
which is probably not the intention of the dataset.

This script corrects this ambiguity by adding a time_bounds variable to define
the time range than each point covers.

Example invocation:

python ./add_core2_time_bounds.py ../input/yatm_1deg/ncar_precip.0001.nc
"""

import sys
import os
import git
import argparse
import datetime
import netCDF4 as nc

def get_history_record(repo_dir):
    """Create a new history record."""

    time_stamp = datetime.datetime.now().isoformat()
    exe = sys.executable
    args = " ".join(sys.argv)
    repo = git.Repo(repo_dir)
    git_url = str(list(repo.remote().urls)[0])
    git_hash = str(repo.heads[0].commit)[0:7]

    entry = "{}: {} {} (Git URL: {}, Git hash: {})".format(time_stamp, exe, args, git_url, git_hash)

    return entry


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input', help="Input CORE file without time_bounds variable.")
    args = parser.parse_args()

    with nc.Dataset(args.input, 'r+') as f:
        try:
            time = f.variables['TIME']
            time_name = 'TIME'
        except KeyError as e:
            time = f.variables['Time']
            time_name = 'Time'
        time.bounds = 'time_bnds'
        if os.path.basename(args.input) == 'runoff.daitren.clim.10FEB2011.nc':
            assert time.units == "days since 0001-01-01 00:00:00"
            time.units = "days since 1900-01-01 00:00:00"

        # Create extra dimension for time_bnds variable
        f.createDimension('time_bnds_dim', 2)
        time_bnds = f.createVariable('time_bnds', 'f8', (time_name, 'time_bnds_dim'))

        if len(time) == 12:
            # Assume this is monthly data and use hard-coded time_bounds. This
            # is necessary because ncar_precip and runoff have different dimensions
            # despite both being monthly.
            time_bnds[:, :] = [[0, 31], [31, 59], [59, 90], [90, 120],
                               [120, 151], [151, 181], [181, 212], [212, 243],
                               [243, 273], [273, 304], [304, 334], [334, 365]]
        else:
            # Calculate time bounds.
            for i, t in enumerate(time[:]):
                if i == 0:
                    time_bnds[i, 0] = 0
                    time_bnds[i, 1] = t*2
                else:
                    time_bnds[i, 0] = time_bnds[i-1, 1]
                    time_bnds[i, 1] = time_bnds[i, 0] + (time[i] - time_bnds[i-1, 1])*2

        # Update the file history.
        my_dir = dir_path = os.path.dirname(os.path.realpath(__file__))
        history = get_history_record(os.path.join(my_dir, '../'))
        if hasattr(f, 'history'):
            f.history = '{} \n {}'.format(f.history, history)
        else:
            f.history = history

if __name__ == "__main__":
    sys.exit(main())
