
import subprocess as sp
import os
import shlex

class TestPrerequisites():

    def test_experiments_exist(self):
        """
        Test that the payu experiment repo has been downloaded.

        To get this test to pass:

        git clone https://github.com/nicholash/payu-experiments.git
        """

        assert(os.path.exists('./payu-experiments/.git'))

    def test_payu_exists(self):
        """
        Test that there is a payu installation.

        To get this test to pass.
        git clone https://github.com/marshallward/payu.git
        Then follow installation instructions.
        """

        cmd = 'which payu'
        ret = sp.call(shlex.split(cmd))
        assert(ret == 0)


    def test_ocean_ice_inputs(self):
        """
        Test that all the necessary ocean and ice inputs exist.

        To get this test to pass:

        Type payu init --laboratory ./lab --model access
        Then populate lab/input with the correct model inputs.
        You may find these at /short/v45/nah599/access/input
        """

        inputs = ['cice', 'core2_nyf_matm', 'mom_om_1440x1080',
                  'cice_cm_1440x1080', 'mom', 'oasis_cm', 'oasis_om',
                  'cice_om_1440x1080', 'mom_cm_1440x1080',
                  'oasis_cm_1440x1080', 'oasis_om_1440x1080']

        for i in inputs:
            assert(os.path.exists(os.path.join('lab/input', i)))

    def test_atm_inputs(self):
        """
        Test that the necessary atm inputs exists.

        To get this test to pass:

        See previous test. 
        """

        assert(os.path.exists('lab/input/um'))


    def test_um_executable_exists(self):
        """
        Since payu cannot build the UM, check that executable
        is here.

        To get this test to pass:
        Talk to Hailin.Yan@csiro.au about how to get a UM executable for
        ACCESS-CM.
        """

        assert(os.path.exists('lab/bin/um7.3.exe'))

