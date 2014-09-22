
from __future__ import print_function

from nose.plugins.attrib import attr

from model_test_setup import ModelTestSetup
import subprocess as sp
import shutil
import os

class TestRunBasic(ModelTestSetup):
    """
    Basic runs. Run and check return code. 
    """

    def __init__(self):
        super(TestRunBasic, self).__init__()

    @attr('fast')
    def test_ACCESS_OM_tiny(self):
        """
        Run the ACCESS-OM_tiny experiment.
        """

        self.do_basic_access_om_run('access-om_tiny')

    @attr('fast')
    def test_ACCESS_CM_tiny(self):
        """
        Run the ACCESS-CM_tiny experiment.
        """

        self.do_basic_access_cm_run('access-cm_tiny')
        

    def test_ACCESS_OM(self):
        """
        Run the ACCESS-OM experiment.
        """

        self.do_basic_access_om_run('access-om')
        

    def test_ACCESS_CM(self):
        """
        Run the ACCESS-CM experiment.
        """

        self.do_basic_access_cm_run('access-cm')


    @attr('slow')
    def test_ACCESS_OM_1440x1080(self):
        """
        Run the ACCESS-OM_1440x1080 experiment.
        """

        self.do_basic_access_om_run('access-om_1440x1080')


    @attr('slow')
    def test_ACCESS_CM_1440x1080(self):
        """
        Run the ACCESS-CM_1440x1080 experiment.
        """

        self.do_basic_access_cm_run('access-cm_1440x1080-0.2_2')
