
from model_test_setup import ModelTestSetup

import subprocess as sp
import os
import shlex

class TestBuild(ModelTestSetup):

    def __init__(self):
        super(TestBuild, self).__init__()

    def test_ACCESS_OM_tiny(self):
        """
        Build executables for ACCESS-OM_tiny experiment.
        """

        os.chdir('payu-experiments/access-om_tiny')
        cmd = 'payu init --laboratory {}'.format(self.lab_dir)
        ret = sp.call(shlex.split(cmd))
        assert(ret == 0)

        os.chdir(self.my_dir)


    def test_ACCESS_CM_tiny(self):
        """
        Build executables for ACCESS-CM_tiny experiment.
        """

        pass

    def test_ACCESS_OM(self):
        """
        Build executables for ACCESS-OM experiment.

        These are the same as ACCESS-OM_tiny
        """

        pass


    def test_ACCESS_CM(self):
        """
        Build executables for ACCESS-CM_tiny experiment.

        These are the same as ACCESS-CM_tiny
        """

        pass

    def test_ACCESS_OM_1440x1080(self):
        """
        Build executables for ACCESS-OM_1440x1080 experiment.
        """

        pass

    def test_ACCESS_CM_1440x1080(self):
        """
        Build executables for ACCESS-CM_1440x1080 experiment.
        """

        pass
