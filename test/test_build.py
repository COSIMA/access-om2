
from __future__ import print_function

import subprocess as sp
import os
import shlex
import pytest

class TestBuild():

    def build_oasis(self):
        return sp.call(['make', '-C', 'src/oasis3-mct'])

    def test_build_matm(self):

        ret = self.build_oasis()
        assert ret == 0
        os.environ['OASIS_ROOT'] = os.path.join(os.getcwd(), 'src/oasis3-mct')

        ret = sp.call(['make', '-C', 'src/matm'])
        assert ret == 0

    def test_build_cice(self):

        ret = self.build_oasis()
        assert ret == 0
        os.environ['OASIS_ROOT'] = os.path.join(os.getcwd(), 'src/oasis3-mct')

        for res in ['1', '01', '025']:
            ret = sp.call(['make', '-C', 'src/cice5', 'access-om{}'.format(res)])
            assert ret == 0

    def test_build_mom(self):

        ret = self.build_oasis()
        assert ret == 0
        os.environ['OASIS_ROOT'] = os.path.join(os.getcwd(), 'src/oasis3-mct')

        mydir = os.getcwd()
        os.chdir('src/mom/exp')
        ret = sp.call(['./MOM_compile.csh', '--type', 'ACCESS-OM', '--platform', 'nci'])

        os.chdir(mydir)
        assert ret == 0
