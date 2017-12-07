
from __future__ import print_function

from exp_test_helper import ExpTestHelper
import os
import numpy as np
import numba
import netCDF4 as nc

EARTH_RADIUS = 6370997.0


def calc_regridding_err(weights, src, dest):
    """
    Calculate the regirdding error.
    """

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

    print('src.shape: {}'.format(src.shape))
    print('n_s, n_b: {} {}'.format(n_s, n_b))
    fstring = 'sum(row[:]) = {}, sum(col[:]) = {}, sum(S[:]) = {}'
    print(fstring.format(np.sum(row[:]), np.sum(col[:]), np.sum(s[:])))

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


class TestRemap():
    def test_jra55_to_01deg(self):
        ret = sp.call(['./get_input_data.py'])
        assert ret == 0

        helper = ExpTestHelper('01deg_jra55_ryf')

        weights = os.path.join(helper.input_path, 'oasis_jra55_to_01deg',
                               'rmp_jrar_to_cict_CONSERV.nc')
        src = np.random.rand(1440, 720)
        dest = remap(src, weights, (3600, 2700))

        rel_err = calc_regridding_err(weights, src, dest)
        print('relative error {}'.format(rel_err))

        assert rel_err < 1e-14

    def test_jra55_to_1deg(self):
        pass

    def test_jra55_to_025deg(self):
        pass


class TestCreateWeights():
    """
    Create weights and compare to existing.
    """

    def test_build_esmf(self):
        """
        Build ESMF
        """

        curdir = os.getcwd()
        contrib_dir = os.path.join(curdir, 'tools', 'contrib')
        os.chdir(contrib_dir)
        ret = sp.call('build_esmf_on_raijin.sh')
        os.chdir(curdir)

        assert ret == 0
        assert os.path.exists(os.path.join(contrib_dir, 'bin', 'ESMF_RegridWeightGen'))

    def test_create_weights(self):
        """
        Create weights
        """

        # Build ESMF_RegridWeightGen if it doesn't already exist
        bpath = os.path.join(contrib_dir, 'bin', 'ESMF_RegridWeightGen')
        if not os.path.exists(bpath):
            self.test_build_esmf()

        ret = sp.call(['./get_input_data.py'])
        assert ret == 0

        cmd = os.path.join(os.getcwd(), 'tools', 'make_remap_weights.py')
        input_dir = os.path.join(os.getcwd(), 'input')
        jra55_dir = '/g/data1/ua8/JRA55-do/RYF/v1-3/'
        ret = sp.call([cmd, input_dir, jra55_dir, '--ocean', 'MOM1'])
        assert ret == 0

        # Check that weights files have been created.
        ocn = ['MOM1']
        # We do not test the more expensive weight creation.
        # ocn = ['MOM1', 'MOM025', 'MOM01']
        atm = ['JRA55', 'JRA55_runoff', 'CORE2']
        method = ['patch', 'conserve2nd']

        for o in ocn:
            for a in atm:
                for m in method:
                    filename = '{}_{}_{}.nc'.format(a, o, m)
                    assert os.path.exists(os.path.join('tools', filename))
