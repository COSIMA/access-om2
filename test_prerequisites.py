
import subprocess as sp
import os

class TestPrerequisites():

    def test_payu_exists(self):
        """
        Test that there is a payu installation.
        """

        ret = sp.call(['which', 'payu'])
        assert(ret == 0)

    def test_experiments_exist(self):
        """
        Test that the payu experiment repo has been downloaded.
        """

        assert(os.path.exists('./payu-experiments'))

    def test_ocean_ice_inputs(self):
        """
        Test that all the necessary ocean and ice inputs exist. 
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
        """

        assert(os.path.exists('lab/input/um'))


    def test_um_executable_exists(self):
        """
        Since payu cannot build the UM, check that executable 
        is here. 
        """

        assert(os.path.exists('lab/bin/um7.3x'))

