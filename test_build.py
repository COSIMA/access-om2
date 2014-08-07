
from model_test_setup import ModelTestSetup

import subprocess as sp

class TestBuild(ModelTestSetup):

    def __init__(self):
        super(TestBuild, self).__init__()

    def test_ACCES_OM_tiny(self):
        """
        Build executables for ACCESS-OM_tiny experiment.
        """

        os.chdir('access/access-om_tiny')
        ret = sp.call('payu init')
        assert(ret == 0)

        os.chdir(self.my_dir)


    def test_ACCES_CM_tiny(self):
        """
        Build executables for ACCESS-CM_tiny experiment.
        """

        pass

    def test_ACCES_OM(self):
        """
        Build executables for ACCESS-OM experiment.

        These are the same as ACCESS-OM_tiny
        """

        pass


    def test_ACCES_CM(self):
        """
        Build executables for ACCESS-CM_tiny experiment.

        These are the same as ACCESS-CM_tiny
        """

        pass

    def test_ACCES_OM_1440x1080(self):
        """
        Build executables for ACCESS-OM_1440x1080 experiment.
        """

        pass

    def test_ACCES_CM_1440x1080(self):
        """
        Build executables for ACCESS-CM_1440x1080 experiment.
        """

        pass
