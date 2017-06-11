
from exp_test_helper import ExpTestHelper

import subprocess as sp

class TestRun():
    """
    Run and check return code.
    """

    def test_run(self):

        ret = sp.call(['./get_input_data.py'])
        assert ret == 0

        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build() == 0
        ret, qso, qse, qsub_files = helper.run()

        assert ret == 0
