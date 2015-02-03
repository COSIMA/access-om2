
import subprocess as sp
import os
import shlex

class TestPrerequisites():


    def test_payu_exists(self):
        """
        Test that there is a payu installation.

        To get this test to pass.
        git clone https://github.com/marshallward/payu.git
        Then follow installation instructions.
        """

        cmd = 'which payu'
        sp.check_output(shlex.split(cmd))


    def test_experiments_exist(self):
        """
        Test that the payu experiment repo has been downloaded.

        To get this test to pass, run either:

        git clone https://github.com/cwsl/payu-experiments.git experiments

        or ./setup.py
        """

        assert(os.path.exists('./experiments/.git'))


    def test_ocean_ice_inputs(self):
        """
        Test that all the necessary ocean and ice inputs exist.

        To get this test to pass, either:

        Type payu init --laboratory ./lab --model access
        Then populate lab/input with the correct model inputs.
        You may find these at /short/public/access-om/

        or, ./setup.py
        """

        inputs = ['cice_om_360x300', 'cice_om_1440x1080',
                  'mom_om_360x300', 'mom_om_1440x1080',
                  'oasis_om_360x300', 'oasis_om_1440x1080',
                  'core2_nyf_matm']

        for i in inputs:
            assert(os.path.exists(os.path.join('lab/input', i)))
