
from exp_test_helper import ExpTestHelper
import os
import glob
import netCDF4 as nc
import numpy as np
import pytest

def find_nearest_index(array, value):
    return (np.abs(array - value)).argmin()

class TestGridMatch():
    """
    Test that MOM and CICE grids match
    """

    @pytest.mark.fast
    def test_mom_and_cice_output_grids(self):
        """
        Compare mom output grid to cice output grid
        """

        helper = ExpTestHelper('minimal_01deg_jra55_ryf_control')
        fo = nc.Dataset(os.path.join(helper.output000, 'ocean', 'ocean_grid.nc'))
        iceh = glob.glob(os.path.join(helper.archive, 'output*', 'ice',
                                        'OUTPUT', 'iceh.*.nc'))
        fi = nc.Dataset(iceh[0])

        fo_tmp = nc.Dataset(os.path.join(helper.mom_input, 'ocean_hgrid.nc'))
        fi_tmp = nc.Dataset(os.path.join(helper.cice_input, 'grid.nc'))

        xtmp = fo_tmp.variables['x'][:]
        ytmp = fo_tmp.variables['y'][:]

        xo_t = fo.variables['geolon_t'][:]
        xo_t[np.where(xo_t < 0)] += 360.0
        yo_t = fo.variables['geolat_t'][:]
        xo_u = fo.variables['geolon_c'][:]
        xo_u[np.where(xo_u < 0)] += 360.0
        yo_u = fo.variables['geolat_c'][:]

        xi_t = fi.variables['TLON'][:].astype('f')
        yi_t = fi.variables['TLAT'][:].astype('f')
        xi_u = fi.variables['ULON'][:].astype('f')
        yi_u = fi.variables['ULAT'][:].astype('f')

        mask = np.logical_or(xo_t.mask, xi_t.mask)
        assert np.ma.allclose(np.ma.array(xo_t, mask=mask), np.ma.array(xi_t, mask=mask), atol=0, rtol=1e-6)
        assert np.ma.allclose(np.ma.array(yo_t, mask=mask), np.ma.array(yi_t, mask=mask), atol=0, rtol=1e-6)
        #assert np.ma.allclose(np.ma.array(xo_u, mask=mask), np.ma.array(xi_u, mask=mask), atol=0, rtol=1e-6)
        #assert np.ma.allclose(np.ma.array(yo_u, mask=mask), np.ma.array(yi_u, mask=mask), atol=0, rtol=1e-6)

        dxo_t = fo.variables['dxt'][:]
        dyo_t = fo.variables['dyt'][:]
        dxo_u = fo.variables['dxu'][:]
        dyo_u = fo.variables['dyu'][:]

        dxi_t = fi.variables['dxt'][:]
        dyi_t = fi.variables['dyt'][:]
        dxi_u = fi.variables['dxu'][:]
        dyi_u = fi.variables['dyu'][:]

        mask = np.logical_or(dxo_t.mask, dxi_t.mask)
        assert np.ma.allclose(np.ma.array(dxo_t, mask=mask), np.ma.array(dxi_t, mask=mask), atol=0, rtol=1e-6)
        #assert np.ma.allclose(np.ma.array(dyo_t, mask=mask), np.ma.array(dyi_t, mask=mask), atol=0, rtol=1e-6)
        assert np.ma.allclose(np.ma.array(dxo_u, mask=mask), np.ma.array(dxi_u, mask=mask), atol=0, rtol=1e-6)
        #assert np.ma.allclose(np.ma.array(dyo_u, mask=mask), np.ma.array(dyi_u, mask=mask), atol=0, rtol=1e-6)

        areao_tmp = fo_tmp.variables['area'][:]

        areao_t = fo.variables['area_t'][:]
        areao_u = fo.variables['area_u'][:]

        areai_t = fi.variables['tarea'][:].astype('f')
        areai_u = fi.variables['uarea'][:].astype('f')

        # Area is difficult to compare because MOM uses dx*dy not the area from
        # ocean_hgrid.nc. We compare cells south of 65N.
        idx = find_nearest_index(yo_t[:, 0], 65.0)

        mask = np.logical_or(areao_t.mask, areai_t.mask)
        assert np.ma.allclose(np.ma.array(areao_t, mask=mask)[:idx, :], np.ma.array(areai_t, mask=mask)[:idx, :])
        #assert np.ma.allclose(np.ma.array(areao_u, mask=mask)[:idx, :], np.ma.array(areai_u, mask=mask)[:idx, :])

        import pdb
        pdb.set_trace()

        fo.close()
        fi.close()

    @pytest.mark.slow
    def test_mom_and_cice_input_grids(self):
        """
        Test that the input grids match
        """

        helper = ExpTestHelper('minimal_01deg_jra55_ryf_control')
        fo = nc.Dataset(os.path.join(helper.mom_input, 'ocean_hgrid.nc'))
        fi = nc.Dataset(os.path.join(helper.cice_input, 'grid.nc'))
        with nc.Dataset(os.path.join(helper.mom_input, 'ocean_mask.nc')) as f:
            mask = 1 - f.variables['mask'][:]

        x = fo.variables['x'][:, :]
        y = fo.variables['y'][:, :]

        # t-cell centres
        xo_t = x[1::2, 1::2]
        yo_t = y[1::2, 1::2]

        xi_t = np.rad2deg(fi.variables['tlon'][:])
        yi_t = np.rad2deg(fi.variables['tlat'][:])

        assert np.allclose(xi_t, xo_t, atol=0, rtol=1e-15)
        assert np.allclose(yi_t, yo_t, atol=0, rtol=1e-15)

        # u-cell centres
        xo_u = x[2::2, 2::2]
        yo_u = y[2::2, 2::2]

        xi_u = np.rad2deg(fi.variables['ulon'][:])
        yi_u = np.rad2deg(fi.variables['ulat'][:])

        #assert np.allclose(xi_u, xo_u, atol=0, rtol=1e-15)
        #assert np.allclose(yi_u, yo_u, atol=0, rtol=1e-15)

        #del x, y, xo_t, yo_t, xi_t, yi_t, xo_u, yo_u, xi_u, yi_u

        # cell area
        # Add up areas, going clockwise from bottom left.
        area = fo.variables['area'][:]
        areao_t = area[0::2, 0::2] + area[1::2, 0::2] + area[1::2, 1::2] + area[0::2, 1::2]

        # These need to wrap around the globe. Copy ocn_area and
        # add an extra column at the end.
        area_ext = np.append(area[:], area[:, 0:1], axis=1)
        areao_u = area_ext[0::2, 1::2] + area_ext[1::2, 1::2] + area_ext[1::2, 2::2] + area_ext[0::2, 2::2]

        areai_t = fi.variables['tarea'][:]
        areai_u = fi.variables['uarea'][:]

        assert np.array_equal(areao_t, areai_t)
        assert np.array_equal(areao_u, areai_u)

        # cell edge length
        # Grab the Northern and Eastern edge distances, not the centre distance,
        # this is what cice should be using.
        dx = fo.variables['dx'][:]
        dy = fo.variables['dy'][:]
        dxo_t = dx[2::2, ::2] + dx[2::2, 1::2]
        dyo_t = dy[::2, 2::2] + dy[1::2, 2::2]

        dxi_t = fi.variables['htn'][:] / 100
        dyi_t = fi.variables['hte'][:] / 100

        assert np.allclose(dxi_t, dxo_t, atol=0, rtol=1e-15)
        assert np.allclose(dyi_t, dyo_t, atol=0, rtol=1e-15)

        import pdb
        pdb.set_trace()

        # angle wrt East
        angleo_t = fo.variables['angle_dx'][1::2, 1::2]
        angleo_u = np.ma.array(fo.variables['angle_dx'][2::2, 2::2], mask=mask)

        anglei_t = np.rad2deg(fi.variables['angleT'][:])
        anglei_u = np.ma.array(np.rad2deg(fi.variables['angle'][:]), mask=mask)

        #import pdb
        #pdb.set_trace()

        assert np.allclose(anglei_t, angleo_t, atol=0, rtol=1e-15)
        # Compare U using the land mask because MOM sets some land only longitudes to zero.
        assert np.ma.allclose(anglei_u, angleo_u, atol=0, rtol=1e-15)

        fo.close()
        fi.close()

    def test_mom_and_cice_mask(self):

        helper = ExpTestHelper('minimal_01deg_jra55_ryf_control')

        with nc.Dataset(os.path.join(helper.mom_input, 'ocean_mask.nc')) as f:
            omask = f.variables['mask'][:]

        with nc.Dataset(os.path.join(helper.cice_input, 'kmt.nc')) as f:
            imask = f.variables['mask'][:]

        import pdb
        pdb.set_trace()

