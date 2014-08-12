
from __future__ import print_function

from nose.plugins.attrib import attr

from model_test_setup import ModelTestSetup
import subprocess as sp
import os
import shlex

class TestBuild(ModelTestSetup):

    def __init__(self):
        super(TestBuild, self).__init__()

    def do_basic_build(self, exp):

        exp_path = os.path.join('payu-experiments/access/', exp)
        os.chdir(exp_path)
        cmd = 'payu build --laboratory {}'.format(self.lab_path)
        ret = sp.call(shlex.split(cmd))

        os.chdir(self.my_path)
        assert(ret == 0)

    @attr('fast')
    def test_ACCESS_OM_tiny(self):
        """
        Build executables for ACCESS-OM_tiny experiment.
        """

        self.do_basic_build('access-om_tiny')

    @attr('fast')
    def test_ACCESS_CM_tiny(self):
        """
        Build executables for ACCESS-CM_tiny experiment.
        """

        self.do_basic_build('access-cm_tiny')

    def test_ACCESS_OM(self):
        """
        Build executables for ACCESS-OM experiment.

        These are the same as ACCESS-OM_tiny
        """

        self.do_basic_build('access-om')


    def test_ACCESS_CM(self):
        """
        Build executables for ACCESS-CM_tiny experiment.

        These are the same as ACCESS-CM_tiny
        """

        self.do_basic_build('access-cm')


    @attr('slow')
    def test_ACCESS_OM_1440x1080(self):
        """
        Build executables for ACCESS-OM_1440x1080 experiment.
        """

        self.do_basic_build('access-om_1440x1080')

    @attr('slow')
    def test_ACCESS_CM_1440x1080(self):
        """
        Build executables for ACCESS-CM_1440x1080 experiment.
        """

        self.do_basic_build('access-cm_1440x1080')
