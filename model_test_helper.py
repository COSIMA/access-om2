
from __future__ import print_function

import subprocess as sp
import shlex
import shutil
import re
import os
import glob
import time
import threading

class ModelTestHelper(object):

    def __init__(self): 

        self.my_path = os.path.dirname(os.path.realpath(__file__))
        self.lab_path = os.path.join(self.my_path, 'lab')
        self.bin_path = os.path.join(self.lab_path, 'bin')
        self.my_lock = threading.Lock()

    def make_paths(self, exp_name):
        paths = {} 
        paths['exp'] = os.path.join(self.my_path, 'payu-experiments/access', exp_name)
        paths['archive'] = os.path.join(self.lab_path, 'archive', exp_name)
        paths['archive_link'] = os.path.join(paths['exp'], 'archive')
        paths['output'] = os.path.join(paths['archive'], 'output000')
        paths['restart'] = os.path.join(paths['archive'], 'restart000')
        paths['stdout'] = os.path.join(paths['output'], 'access.out')
        paths['stderr'] = os.path.join(paths['output'], 'access.err')

        return paths


    def pre_build_cleanup(self, exes):

        for e in exes:
            if os.path.exists(e):
                os.remove(e)

    def post_build_checks(self, exes):

        for e in exes:
            assert(os.path.exists(e))

    def do_basic_build(self, exp):

        exp_path = os.path.join('payu-experiments/access/', exp)
        ret = self.build(exp_path)
        os.chdir(self.my_path)
        assert(ret == 0)


    def pre_run_checks(self, paths):

        # No model output should exist.
        assert(not os.path.exists(paths['archive']))

    def post_run_checks(self, paths):

        # Model output should exist.
        assert(os.path.exists(paths['output']))
        assert(os.path.exists(paths['restart']))
        assert(os.path.exists(paths['stdout']))
        assert(os.path.exists(paths['stderr']))


    def post_run_cleanup(self, paths, qsub_files):

        # Do some clean-up
        shutil.rmtree(paths['archive'])
        os.remove(paths['archive_link'])
        for f in qsub_files:
            os.remove(f)


    def do_basic_access_cm_run(self, exp):

        paths = self.make_paths(exp)
        
        self.pre_run_checks(paths)
        ret, _, _, qsub_files = self.run(paths['exp'], self.lab_path)
        assert(ret == 0)
        self.post_run_checks(paths)

        with open(paths['stdout'], 'r') as f:
            s = f.read()
            assert('MOM4: --- completed ---' in s)

        self.post_run_cleanup(paths, qsub_files)


    def do_basic_access_om_run(self, exp):

        paths = self.make_paths(exp)
        
        self.pre_run_checks(paths)
        ret, _, _, qsub_files = self.run(paths['exp'], self.lab_path)
        assert(ret == 0)
        self.post_run_checks(paths)

        with open(paths['stdout'], 'r') as f:
            s = f.read()
            assert('MOM4: --- completed ---' in s)
            assert('********** End of MATM **********' in s)

        self.post_run_cleanup(paths, qsub_files)


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


    def build(self, exp_path):

        # Need to lock around the chdirs. 
        self.my_lock.acquire()

        cur_dir = os.getcwd()
        os.chdir(exp_path)
        cmd = 'payu build --laboratory {}'.format(self.lab_path)
        ret = sp.call(shlex.split(cmd))

        os.chdir(cur_dir)

        self.my_lock.release()
        return ret

    def run(self, expt_path, lab_path):
        """
        Run the given experiment using payu and check output.

        """

        # Need to lock around the chdirs. 
        self.my_lock.acquire()

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
            self.my_lock.release()
            return 1, None, None, None

        self.my_lock.release()

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

