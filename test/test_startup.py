
from __future__ import print_function

import netCDF4 as nc
import os
import filecmp
from nose.plugins.attrib import attr

from exp_test_helper import ExpTestHelper


class TestStartUp(ExpTestHelper):

    def test_coupling_restarts_change(self):
        """
        Check that the coupling restarts change between subsequent runs. If not
        they're not being regenerated properly.
        """

        exps = ['cm_360x300-test', 'om_360x300-test']
        cpl_restarts = ['a2i.nc', 'i2a.nc', 'o2i.nc', 'i2o.nc']
        for e in exps:
            for r in cpl_restarts:
                run0_paths = self.make_paths(e, 0)
                run1_paths = self.make_paths(e, 1)

                self.get_most_recent_run_num(run0_paths['archive'])

                file0 = os.path.join(run0_paths['restart'], 'coupler', r)
                file1 = os.path.join(run1_paths['restart'], 'coupler', r)

                assert(not filecmp.cmp(file0, file1))

    def test_coupling_restarts_loaded(self):
        """
        Check that the fields on the first timestep are
        the same as the OASIS restarts.
        """

        pass
