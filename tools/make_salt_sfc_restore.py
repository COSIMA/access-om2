#!/usr/bin/env python

import numpy as np
import sys
import numba
import os
import argparse
import netCDF4 as nc
import shutil
from scipy.ndimage.filters import uniform_filter

"""
Create MOM salt_sfc_restore.nc file from WOA
"""

def calc_regridding_err(weights, src, dest):
    """
    Calculate the regridding error.
    """

    EARTH_RADIUS = 6370997.0

    with nc.Dataset(weights) as f:
        try:
            area_a = f.variables['area_a'][:]
        except KeyError as e:
            area_a = f.variables['src_grid_area'][:]
        area_a = area_a.reshape(src.shape[0], src.shape[1])
        area_a = area_a*EARTH_RADIUS**2

        try:
            area_b = f.variables['area_b'][:]
        except KeyError as e:
            area_b = f.variables['dst_grid_area'][:]
        area_b = area_b.reshape(dest.shape[0], dest.shape[1])
        area_b = area_b*EARTH_RADIUS**2

        try:
            frac_a = f.variables['frac_a'][:]
        except KeyError as e:
            frac_a = f.variables['src_grid_frac'][:]
        frac_a = frac_a.reshape(src.shape[0], src.shape[1])

        try:
            frac_b = f.variables['frac_b'][:]
        except KeyError as e:
            frac_b = f.variables['dst_grid_frac'][:]
        frac_b = frac_b.reshape(dest.shape[0], dest.shape[1])

    # Calculation of totals here.
    # http://www.earthsystemmodeling.org/esmf_releases/non_public/ESMF_5_3_0/ESMC_crefdoc/node3.html
    src_tot = np.sum(src[:, :] * area_a[:, :] * frac_a[:, :])
    dest_tot = np.sum(dest[:, :] * area_b[:, :])
    rel_err = abs(src_tot - dest_tot) / dest_tot

    return rel_err

@numba.jit
def apply_weights(src, dest_shape, n_s, n_b, row, col, s):
    """
    Apply ESMF regirdding weights.
    """

    dest = np.ndarray(dest_shape).flatten()
    dest[:] = 0.0
    src = src.flatten()

    for i in range(n_s):
        dest[row[i]-1] = dest[row[i]-1] + s[i]*src[col[i]-1]

    return dest.reshape(dest_shape)


def remap(src_data, weights, dest_shape):
    """
    Regrid a 2d field and see how it looks.
    """

    dest_data = np.ndarray(dest_shape)

    with nc.Dataset(weights) as wf:
        try:
            n_s = wf.dimensions['n_s'].size
        except KeyError as e:
            n_s = wf.dimensions['num_links'].size
        try:
            n_b = wf.dimensions['n_b'].size
        except KeyError as e:
            n_b = wf.dimensions['dst_grid_size'].size
        try:
            row = wf.variables['row'][:]
        except KeyError as e:
            row = wf.variables['dst_address'][:]
        try:
            col = wf.variables['col'][:]
        except KeyError as e:
            col = wf.variables['src_address'][:]

        s = wf.variables['S'][:]

    dest_data[:, :] = apply_weights(src_data[:, :], dest_data.shape,
                                    n_s, n_b, row, col, s)
    return dest_data


def create_weights():
    raise NotImplementedError


def smooth2d(src):

    tmp_src = np.ndarray((src.shape[0] + 6, src.shape[1]))

    # Window size
    ws = 3

    tmp_src[ws:-ws, :] = src[:, :]
    tmp_src[:ws, :] = src[-ws:, :]
    tmp_src[-ws:, :] = src[:3, :]

    dest = uniform_filter(tmp_src, size=ws, mode='nearest')
    return dest[ws:-ws, :]


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('woa_input', help='The WOA input file.')
    parser.add_argument('resolution', help='Resolution of the output can be 1deg, 025deg or 01deg')
    parser.add_argument('old_salt_sfc_restore',
                        help='The old salt sfc restoring file. Needed for metadata.')
    parser.add_argument('output', help='salt_sfc_restore.nc file for MOM5')
    parser.add_argument('--interpolation_weights', default=None,
                        help='Interpolation weights, file if not given this will be created.')

    args = parser.parse_args()

    assert args.resolution in ['1deg', '025deg', '01deg']

    if args.interpolation_weights is None:
        weights = create_weights()
    else:
        weights = args.interpolation_weights

    if args.resolution == '1deg':
        dest_res = (300, 360)
    elif args.resolution == '025deg':
        dest_res = (1080, 1440)
    else: 
        dest_res = (2700, 3600)

    with nc.Dataset(args.woa_input) as f:
        src = f.variables['so'][:]

    dest = np.zeros((src.shape[0], dest_res[0], dest_res[1]))

    for t in range(src.shape[0]):
        smooth_src = smooth2d(src[t, :, :])
        dest[t, :, :] = remap(smooth_src, weights, dest_res)

        rel_err = calc_regridding_err(weights, smooth_src, dest[t, :, :])
        print('relative error {}'.format(rel_err))

        assert rel_err < 1e-14

    shutil.copyfile(args.old_salt_sfc_restore, args.output)
    with nc.Dataset(args.output, 'r+') as f:
        import pdb
        pdb.set_trace()
        f.variables['salt'][:] = dest

if __name__ == '__main__':
    sys.exit(main())
