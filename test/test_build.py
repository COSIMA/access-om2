
import pytest
from exp_test_helper import ExpTestHelper

class TestBuild():

    @pytest.mark.1deg
    def test_build_libaccessom2(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        exe, ret = helper.build_libaccessom2()
        assert ret == 0

    @pytest.mark.1deg
    def test_build_1deg_cice(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        exe, ret = helper.build_cice()
        assert ret == 0

    @pytest.mark.025deg
    def test_build_025deg_cice(self):
        helper = ExpTestHelper('025deg_jra55_ryf')
        exe, ret = helper.build_cice()
        assert ret == 0

    @pytest.mark.01deg
    def test_build_01deg_cice(self):
        helper = ExpTestHelper('01deg_jra55_ryf')
        exe, ret = helper.build_cice()
        assert ret == 0

    @pytest.mark.1deg
    def test_build_mom(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        exe, ret = helper.build_mom()
        assert ret == 0
