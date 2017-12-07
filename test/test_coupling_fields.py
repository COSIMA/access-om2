
from __future__ import print_function

import os
import netCDF4 as nc

from exp_test_helper import ExpTestHelper


class TestCouplingFields(ExpTestHelper):

    def __init__(self):
        super(TestCouplingFields, self).__init__()

    def test_swflx(self):
        """
        Compare short wave flux over a geographic area between low and hi res
        models.
        """

        hi_paths = self.make_paths('cm_1440x1080-test')
        lo_paths = self.make_paths('cm_360x300-test')

        hi_fields = os.path.join(hi_paths['output'], 'ice',
                                 'fields_a2i_in_ice.nc')
        lo_fields = os.path.join(lo_paths['output'], 'ice',
                                 'fields_a2i_in_ice.nc')
        f_hi = nc.Dataset(hi_fields)
        f_hi.close()
        f_lo = nc.Dataset(lo_fields)
        f_lo.close()
