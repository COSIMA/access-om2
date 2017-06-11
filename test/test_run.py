
from __future__ import print_function

import shutil
import os
from exp_test_helper import ExpTestHelper

class TestRun():
    """
    Run and check return code.
    """

    def test_run(self):

        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build() == 0

        for k in tests.keys():
            yield self.check_run, k
