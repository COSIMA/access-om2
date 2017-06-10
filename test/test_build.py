
from __future__ import print_function

import subprocess as sp
import os
import shlex

class TestBuild():

    def test_build_matm(self):

        mydir = os.getcwd()
        os.chdir('src/matm')

        ret = sp.call(['make'])
        os.chdir(mydir)
        assert ret == 0

    def test_build_cice(self):

        for res in ['1', '01', '025']:
            mydir = os.getcwd()
            os.chdir('src/cice5')
            ret = sp.call(['make', 'access-om{}'.format(res)])

            os.chdir(mydir)
            assert ret == 0

    def test_build_mom(self):

      mydir = os.getcwd()
      os.chdir('src/mom/exp')

      ret = sp.call(['./MOM_compile.csh', '--type', 'ACCESS-OM', '--platform', 'nci']) 

      os.chdir(mydir)
      assert ret == 0
