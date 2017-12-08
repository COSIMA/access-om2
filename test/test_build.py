
from __future__ import print_function

import subprocess as sp
import os
import shlex
import pytest

from exp_test_helper import ExpTestHelper


class TestBuild():

    def test_build_oasis(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_oasis() == 0

    def test_build_matm(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_matm() == 0

    def test_build_cice(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_cice5() == 0

    def test_build_mom(self):
        helper = ExpTestHelper('1deg_jra55_ryf')
        assert helper.build_mom() == 0
