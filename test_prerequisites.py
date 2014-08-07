
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

    def test_laboratory_exist(self):
        """
        Test that all the necessary inputs exist. 
        """
        
        inputs = ['cice', 'core2_nyf_matm', 'mom_om_1440x1080', 'um',
                  'cice_cm_1440x1080', 'mom', 'oasis_cm', 'oasis_om',
                  'cice_om_1440x1080', 'mom_cm_1440x1080',
                  'oasis_cm_1440x1080', 'oasis_om_1440x1080']

        for i in inputs:
            assert(os.path.exists(os.path.join('access/input', i)))

    def test_um_executable_exists(self):
        """
        Since payu cannot build the UM, check that executable 
        is here. 
        """

        assert(os.path.exists('access/bin/um7.3x'))

