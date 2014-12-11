
from __future__ import print_function

from nose.plugins.attrib import attr

import netCDF4 as nc

from model_test_helper import ModelTestHelper

class TestCouplingFields(ModelTestHelper):

    def __init__(self):
        super(TestCouplingFields, self).__init__()

    @attr('slow')
    def test_swflx():
        """
        Compare short wave flux over a geographic area between low and hi res
        models.
        """

        hi_fields = os.path.join(self.paths['cm_1440x1080-test']['output'], 'ice',
                                 'fields_a2i_in_ice.nc')
        lo_fields = os.path.join(self.paths['cm_360x300-test']['output'], 'ice',
                                 'fields_a2i_in_ice.nc')
        f_hi = nc.Dataset(hi_fields)
        f_hi.close()
        f_lo = nc.Dataset(lo_fields)
        f_lo.close()
