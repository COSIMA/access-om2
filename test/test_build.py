
from exp_test_helper import ExpTestHelper

class TestBuild():

    def test_build_libaccessom2(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_libaccessom2() == 0

    def test_build_cice(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_cice5() == 0

    def test_build_mom(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_mom() == 0
