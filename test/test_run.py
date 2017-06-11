
from exp_test_helper import ExpTestHelper

class TestRun():
    """
    Run and check return code.
    """

    def test_run(self):

        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build() == 0
        ret, qso, qse, qsub_files = helper.run()

        assert ret == 0
