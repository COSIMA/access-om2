
from __future__ import print_function

from nose.plugins.attrib import attr

from model_test_helper import ModelTestHelper

class TestBasicRun(ModelTestHelper):
    """
    Basic runs. Run and check return code.
    """

    def __init__(self):
        super(TestBasicRun, self).__init__()

    @attr('fast')
    def test_ACCESS_OM_tiny(self):
        """
        Run a tiney ACCESS-OM experiment.
        """

        self.do_basic_access_om_run('om_360x300-tiny')

    @attr('fast')
    def test_ACCESS_CM_tiny(self):
        """
        Run a tiny ACCESS-CM experiment.
        """

        self.do_basic_access_cm_run('cm_360x300-tiny')


    def test_ACCESS_OM(self):
        """
        Run the ACCESS-OM experiment.
        """

        self.do_basic_access_om_run('om_360x300-system_test')


    def test_ACCESS_CM(self):
        """
        Run the ACCESS-CM experiment.
        """

        self.do_basic_access_cm_run('cm_360x300-system_test')


    @attr('slow')
    def test_ACCESS_OM_1440x1080(self):
        """
        Run the ACCESS-OM_1440x1080 experiment.
        """

        self.do_basic_access_om_run('om_1440x1080-system_test')


    @attr('slow')
    def test_ACCESS_CM_1440x1080(self):
        """
        Run the ACCESS-CM_1440x1080 experiment.
        """

        self.do_basic_access_cm_run('cm_1440x1080-system_test')
