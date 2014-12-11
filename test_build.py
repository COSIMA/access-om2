
from __future__ import print_function

from nose.plugins.attrib import attr

from model_test_helper import ModelTestHelper
import subprocess as sp
import os
import shlex

class TestBuild(ModelTestHelper):

    def __init__(self):
        super(TestBuild, self).__init__()

    def test_ACCESS_OM(self):
        """
        Build executables for ACCESS-OM_tiny experiment.
        """

        matm_exe = os.path.join(self.bin_path, 'matm_nt62.exe')
        cice_exe = os.path.join(self.bin_path, 'cice_access-om_360x300_6p.exe')
        mom_exe = os.path.join(self.bin_path, 'fms_ACCESS-OM.x')
        exes = [matm_exe, cice_exe, mom_exe]

        self.do_basic_build('om_360x300-test')
        self.post_build_checks(exes)

    def test_ACCESS_CM(self):
        """
        Build executables for ACCESS-CM_tiny experiment.
        """

        cice_exe = os.path.join(self.bin_path, 'cice_access-cm_360x300_6p.exe')
        mom_exe = os.path.join(self.bin_path, 'fms_ACCESS-CM.x')
        exes = [cice_exe, mom_exe]

        self.do_basic_build('cm_360x300-test')
        self.post_build_checks(exes)


    @attr('slow')
    def test_ACCESS_OM_1440x1080(self):
        """
        Build executables for ACCESS-OM_1440x1080 experiment.
        """

        matm_exe = os.path.join(self.bin_path, 'matm_nt62.exe')
        cice_exe = os.path.join(self.bin_path, 'cice_access-om_1440x1080_192p.exe')
        mom_exe = os.path.join(self.bin_path, 'fms_ACCESS-OM.x')
        exes = [matm_exe, cice_exe, mom_exe]

        self.do_basic_build('om_1440x1080-test')
        self.post_build_checks(exes)


    @attr('slow')
    def test_ACCESS_CM_1440x1080(self):
        """
        Build executables for ACCESS-CM_1440x1080 experiment.
        """

        cice_exe = os.path.join(self.bin_path, 'cice_access-cm_1440x1080_192p.exe')
        mom_exe = os.path.join(self.bin_path, 'fms_ACCESS-CM.x')
        exes = [cice_exe, mom_exe]

        self.do_basic_build('cm_1440x1080-test')
        self.post_build_checks(exes)
