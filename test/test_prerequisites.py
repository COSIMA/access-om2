
import subprocess as sp
import os


class TestPrerequisites():

    def test_payu(self):
        """
        Test that there is a payu installation.

        To get this test to pass.
        git clone https://github.com/marshallward/payu.git
        Then follow installation instructions.
        """

        ret = sp.call(['which', 'payu'])
        assert ret == 0

    def test_inputs(self):
        """
        Test that all the necessary inputs exist.

        To get this test to pass, either:

        ./get_input_data.py
        """

        assert os.path.exists('get_input_data.py')

        ret = sp.call(['./get_input_data.py'])
        assert ret == 0

        inputs = ['cice_01deg', 'cice_025deg', 'cice_1deg',
                  'core_nyf', 'mom_01deg', 'mom_025deg',
                  'mom_1deg', 'oasis_core_to_1deg',
                  'yatm_1deg', 'yatm_025deg', 'yatm_01deg']

        for i in inputs:
            assert os.path.exists(os.path.join('input', i))
