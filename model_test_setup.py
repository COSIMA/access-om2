
from __future__ import print_function

import subprocess as sp
import shlex
import os
import time

class ModelTestSetup(object):

    def __init__(self): 

        self.my_dir = os.path.dirname(os.path.realpath(__file__))
        self.lab_dir = os.path.join(self.my_dir, 'lab')

    def download_input_data(self, exp):
        """
        Download the experiment input data. 
        """

        raise NotImplementedError
        

    def wait(self, run_id):
        """
        Wait for the qsub job to terminate. 
        """

        while True:
            time.sleep(5)
            qsub_out = ''
            try:
                qsub_out = sp.check_output(['qstat', run_id], stderr=sp.STDOUT)
            except sp.CalledProcessError as err:
                qsub_out = err.output

            print('qsub_out = {}'.format(qsub_out))
            if 'Job has finished' in qsub_out:
                break



    def run(self, expt_path, lab_path='lab'):
        """
        Run the given experiment using payu and check output.
        """

        os.chdir(expt_path)
        cmd = 'payu run -n 1 --laboratory {}'.format(lab_path)
        run_id = sp.check_output(shlex.split(cmd))
        run_id = run_id.strip()

        self.wait(run_id)

        # Read all the output files and return to caller.
        import pdb
        pdb.set_trace()


