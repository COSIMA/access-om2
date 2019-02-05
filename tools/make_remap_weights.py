#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import shutil
import shlex
import argparse
import netCDF4 as nc
import numpy as np
import tempfile
import subprocess as sp
import multiprocessing as mp

my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_dir, './esmgrids'))

from esmgrids.mom_grid import MomGrid  # noqa
from esmgrids.core2_grid import Core2Grid  # noqa
from esmgrids.jra55_grid import Jra55Grid  # noqa
from esmgrids.jra55_river_grid import Jra55RiverGrid  # noqa
from esmgrids.daitren_runoff_grid import DaitrenRunoffGrid  # noqa

"""
This script makes all of the remapping weights for ACCESS-OM2.

Run example:

./make_remap_weights.py /short/x77/nah599/access-om2/input/ \
/g/data1/ua8/JRA55-do/RYF/v1-3/
"""

def convert_to_scrip_output(weights):

    my_dir = os.path.dirname(os.path.realpath(__file__))

    _, new_weights = tempfile.mkstemp(suffix='.nc', dir=my_dir)
    # So that ncrename doesn't prompt for overwrite.
    os.remove(new_weights)

    cmdstring = ('ncrename -d n_a,src_grid_size -d n_b,dst_grid_size -d n_s,'
                 'num_links -d nv_a,src_grid_corners -d nv_b,dst_grid_corner'
                 's -v yc_a,src_grid_center_lat -v yc_b,dst_grid_center_lat '
                 '-v xc_a,src_grid_center_lon -v xc_b,dst_grid_center_lon -v'
                 ' yv_a,src_grid_corner_lat -v xv_a,src_grid_corner_lon -v y'
                 'v_b,dst_grid_corner_lat -v xv_b,dst_grid_corner_lon -v mas'
                 'k_a,src_grid_imask -v mask_b,dst_grid_imask -v area_a,src_'
                 'grid_area -v area_b,dst_grid_area -v frac_a,src_grid_frac '
                 '-v frac_b,dst_grid_frac -v col,src_address -v row,dst_addr'
                 'ess {} {}')
    cmd = cmdstring.format(weights, new_weights)

    try:
        sp.check_output(shlex.split(cmd))
    except sp.CalledProcessError as e:
        print(cmd, file=sys.stderr)
        print(e.output, file=sys.stderr)
        return None

    # Fix the dimension of the remap_matrix.
    with nc.Dataset(weights) as f_old, nc.Dataset(new_weights, 'r+') as f_new:
        remap_matrix = f_new.createVariable('remap_matrix',
                                            'f8', ('num_links', 'num_wgts'))
        remap_matrix[:, 0] = f_old.variables['S'][:]

    os.remove(weights)

    return new_weights


def create_weights(src_grid, dest_grid, npes, method,
                   ignore_unmapped=False,
                   unmasked_src=True, unmasked_dest=False):

    my_dir = os.path.dirname(os.path.realpath(__file__))

    _, src_grid_scrip = tempfile.mkstemp(suffix='.nc', dir=my_dir)
    _, dest_grid_scrip = tempfile.mkstemp(suffix='.nc', dir=my_dir)
    _, regrid_weights = tempfile.mkstemp(suffix='.nc', dir=my_dir)

    if unmasked_src:
        src_grid.write_scrip(src_grid_scrip, write_test_scrip=False,
                             mask=np.zeros_like(src_grid.mask_t, dtype=int))
    else:
        src_grid.write_scrip(src_grid_scrip, write_test_scrip=False)

    if unmasked_dest:
        dest_grid.write_scrip(dest_grid_scrip, write_test_scrip=False,
                              mask=np.zeros_like(dest_grid.mask_t, dtype=int))
    else:
        dest_grid.write_scrip(dest_grid_scrip, write_test_scrip=False)

    if ignore_unmapped:
        ignore_unmapped = ['--ignore_unmapped']
    else:
        ignore_unmapped = []

    try:
        cmd = ['mpirun', '-np', str(npes), 'ESMF_RegridWeightGen'] + \
              ['--netcdf4',
               '-s', src_grid_scrip,
               '-d', dest_grid_scrip, '-m', method,
               '-w', regrid_weights] + ignore_unmapped
        print(cmd)
        sp.check_output(cmd)
    except sp.CalledProcessError as e:
        print("Error: ESMF_RegridWeightGen failed ret {}".format(e.returncode),
              file=sys.stderr)
        print(e.output, file=sys.stderr)
        log = 'PET0.RegridWeightGen.Log'
        if os.path.exists(log):
            print('Contents of {}:'.format(log), file=sys.stderr)
            with open(log) as f:
                print(f.read(), file=sys.stderr)
        return None

    os.remove(src_grid_scrip)
    os.remove(dest_grid_scrip)

    return regrid_weights


def find_grid_defs(input_dir, jra55_input, core_input):
    """
    Return a dictionary containing the grid definition files.
    """

    d = {}
    d['MOM1'] = (os.path.join(input_dir, 'mom_1deg', 'ocean_hgrid.nc'),
                 os.path.join(input_dir, 'mom_1deg', 'ocean_mask.nc'))
    d['MOM025'] = (os.path.join(input_dir, 'mom_025deg', 'ocean_hgrid.nc'),
                   os.path.join(input_dir, 'mom_025deg', 'ocean_mask.nc'))
    d['MOM01'] = (os.path.join(input_dir, 'mom_01deg', 'ocean_hgrid.nc'),
                  os.path.join(input_dir, 'mom_01deg', 'ocean_mask.nc'))
    d['CORE2'] = os.path.join(core_input, 't_10.0001.nc')
    d['JRA55'] = os.path.join(jra55_input, 'RYF.t_10.1990_1991.nc')
    d['JRA55_runoff'] = os.path.join(jra55_input,
                                     'RYF.runoff_all.1990_1991.nc')
    d['Daitren_runoff'] = os.path.join(core_input, 'runoff.daitren.clim.10FEB2011.nc')

    return d


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help="""
                        The ACCESS-OM2 input directory.""")
    parser.add_argument('jra55_input', help="""
                        The JRA55 input directory.""")
    parser.add_argument('core_input', help="""
                        The CORE input directory.""")
    parser.add_argument('--atm', default=None, help="""
                        Atmosphere grid to regrid from, can be one of:
                        CORE2, JRA55, JRA55_runoff, Daitren_runoff""")
    parser.add_argument('--ocean', default=None, help="""
                        Ocean grid to regrid to, can be one of:
                        MOM1, MOM01, MOM025""")
    parser.add_argument('--method', default=None, help="""
                        The interpolation method to use, can be patch or conserve2nd""")
    parser.add_argument('--npes', default=None, help="""
                        The number of PEs to use.""")

    args = parser.parse_args()
    atm_options = ['JRA55', 'JRA55_runoff', 'CORE2', 'Daitren_runoff']
    ocean_options = ['MOM1', 'MOM025', 'MOM01']
    method_options = ['patch', 'conserve2nd']

    if args.atm is None:
        args.atm = atm_options
    else:
        if args.atm not in atm_options:
            print("Error: bad atm grid.", file=sys.stderr)
            parser.print_help()
            return 1
        args.atm = [args.atm]

    if args.ocean is None:
        args.ocean = ocean_options
    else:
        if args.ocean not in ocean_options:
            print("Error: bad atm grid.", file=sys.stderr)
            parser.print_help()
            return 1
        args.ocean = [args.ocean]

    if args.method is None:
        args.method = method_options
    else:
        args.method = [args.method]

    if args.npes is None:
        import multiprocessing as mp
        args.npes = mp.cpu_count() // 2

    grid_file_dict = find_grid_defs(args.input_dir, args.jra55_input, args.core_input)

    for ocean in args.ocean:
        umask_file = grid_file_dict[ocean][1]
        dest_grid = MomGrid.fromfile(grid_file_dict[ocean][0],
                                     mask_file=umask_file)
        for atm in args.atm:

            if atm == 'CORE2':
                src_grid = Core2Grid(grid_file_dict[atm])
            elif atm == 'Daitren_runoff':
                src_grid = DaitrenRunoffGrid(grid_file_dict[atm])
            elif atm == 'JRA55':
                src_grid = Jra55Grid(grid_file_dict[atm])
            elif atm == 'JRA55_runoff':
                src_grid = Jra55RiverGrid(grid_file_dict[atm], calc_areas=False)
            else:
                print('Unrecognised atmosphere grid: {}'.format(atm))
                return 1

            for method in args.method:

                weights = create_weights(src_grid, dest_grid, args.npes,
                                         method)
                if not weights:
                    return 1
                weights = convert_to_scrip_output(weights)
                if not weights:
                    return 1

                shutil.move(weights, '{}_{}_{}.nc'.format(atm, ocean, method))

    return 0

if __name__ == "__main__":
    sys.exit(main())
