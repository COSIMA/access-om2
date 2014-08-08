
from __future__ import print_function

from model_test_setup import ModelTestSetup

class TestRun(ModelTestSetup):

    def __init__(self):
        super(TestRun, self).__init__()

    def test_ACCESS_OM_tiny(self):
        """
        Run the ACCESS-OM_tiny experiment.
        """

        ret, sout, serr = self.run('payu-experiments/access/access-om_tiny')


    def test_ACCESS_CM_tiny(self):
        """
        Run the ACCESS-CM_tiny experiment.
        """

        pass

    def test_ACCESS_OM(self):
        """
        Run the ACCESS-OM experiment.
        """

        pass


    def test_ACCESS_CM(self):
        """
        Run the ACCESS-CM experiment.
        """

        pass

    def test_ACCESS_OM_1440x1080(self):
        """
        Run the ACCESS-OM_1440x1080 experiment.
        """

        pass

    def test_ACCESS_CM_1440x1080(self):
        """
        Run the ACCESS-CM_1440x1080 experiment.
        """

        pass
