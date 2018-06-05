
from exp_test_helper import run_exp

import pytest


class TestRun():
    """
    Run and check return code.
    """

    @pytest.mark.fast
    def test_1deg_jra55_ryf_run(self):
        run_exp('1deg_jra55_ryf')

    @pytest.mark.slow
    def test_1deg_jra55_iaf_run(self):
        run_exp('1deg_jra55_iaf')

    @pytest.mark.slow
    def test_1deg_core_run(self):
        run_exp('1deg_core_nyf')

    @pytest.mark.slow
    def test_slow_run(self):
        run_exp('025deg_jra55_ryf')
