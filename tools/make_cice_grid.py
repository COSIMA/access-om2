#!/usr/bin/env python

import sys
import os
import argparse

my_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_dir, 'esmgrids'))

from esmgrids.mom_grid import MomGrid  # noqa
from esmgrids.cice_grid import CiceGrid  # noqa

"""
Create CICE grid.nc and kmt.nc from MOM ocean_hgrid.nc and ocean_mask.nc
"""

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('ocean_hgrid', help='ocean_mask.nc file')
    parser.add_argument('ocean_mask', help='ocean_hgrid.nc file')

    args = parser.parse_args()

    mom = MomGrid.fromfile(args.ocean_hgrid, mask_file=args.ocean_mask)

    # FIXME:
    # MOM dx is at the cell centre while HTN is on the Northern boundary
    # MOM dy is at the cell centre while HTE is on the Eastern boundary
    cice = CiceGrid.fromgrid(mom)

    grid_file = os.path.join('grid.nc')
    mask_file = os.path.join('kmt.nc')
    cice.write(grid_file, mask_file)

if __name__ == '__main__':
    sys.exit(main())
