
from __future__ import print_function

import subprocess as sp
import shlex
import re
import os
import glob
import time

class ModelTestSetup(object):

    def __init__(self): 

        self.my_path = os.path.dirname(os.path.realpath(__file__))
        self.lab_path = os.path.join(self.my_path, 'lab')
        self.bin_path = os.path.join(self.lab_path, 'bin')

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

            if 'Job has finished' in qsub_out:
                break


    def run(self, expt_path, lab_path):
        """
        Run the given experiment using payu and check output.

        """

        # Change to experiment directory and run. 
        try:
            os.chdir(expt_path)
            cmd = 'payu sweep --laboratory {}'.format(lab_path)
            sp.check_output(shlex.split(cmd))
            cmd = 'payu run -n 1 --laboratory {}'.format(lab_path)
            run_id = sp.check_output(shlex.split(cmd))
            run_id = run_id.strip()
            os.chdir(self.my_path)
        except sp.CalledProcessError as err:
            os.chdir(self.my_path)
            return 1, None, None, None

        self.wait(run_id)
        run_id = run_id.split('.')[0]

        output_files = []
        # Read qsub stdout file
        stdout_filename = glob.glob(os.path.join(expt_path,
                                                '*.o{}'.format(run_id)))
        if len(stdout_filename) != 1:
            return 1, None, None, None

        stdout_filename = stdout_filename[0]
        output_files.append(stdout_filename)
        stdout = ''
        with open(stdout_filename, 'r') as f:
            stdout = f.read()

        # Read qsub stderr file
        stderr_filename = glob.glob(os.path.join(expt_path,
                                                '*.e{}'.format(run_id)))
        stderr = ''
        if len(stderr_filename) == 1:
            stderr_filename = stderr_filename[0]
            output_files.append(stderr_filename)
            with open(stderr_filename, 'r') as f:
                stderr = f.read()

        # Read the qsub id of the collate job from the stdout. 
        # Payu puts this here. 
        m = re.search(r'\n(\d{7}.r-man2)\n', stdout)
        if m is None:
            return 1, stdout, stderr, output_files

        # Wait for the collate to complete. 
        run_id = m.group(1)
        self.wait(run_id)

        # Return files created by qsub so caller can read or delete.
        collate_files = os.path.join(expt_path, '*.[oe]{}'.format(run_id))
        output_files += glob.glob(collate_files)
        
        return 0, stdout, stderr, output_files

