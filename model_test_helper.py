
from __future__ import print_function

import subprocess as sp
import sys
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

    def make_paths(self, exp_name, run_num=0):
        paths = {}
        run_num = str(run_num).zfill(3)

        paths['exp'] = os.path.join(self.my_path, 'payu-experiments/access',
                                    exp_name)
        paths['archive'] = os.path.join(self.lab_path, 'archive', exp_name)
        paths['archive_link'] = os.path.join(paths['exp'], 'archive')
        paths['output'] = os.path.join(paths['archive'], 'output' + run_num)
        paths['restart'] = os.path.join(paths['archive'], 'restart' + run_num)
        paths['stdout'] = os.path.join(paths['output'], 'access.out')
        paths['stderr'] = os.path.join(paths['output'], 'access.err')

        paths['stdout_runtime'] = os.path.join(paths['exp'], 'access.out')
        paths['stderr_runtime'] = os.path.join(paths['exp'], 'access.err')

        return paths

    def post_build_checks(self, exes):

        for e in exes:
            assert(os.path.exists(e))

    def do_basic_build(self, exp):

        exp_path = os.path.join('payu-experiments/access/', exp)
        ret = self.build(exp_path)
        os.chdir(self.my_path)
        assert(ret == 0)

    def print_output(self, files):

        for file in files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    print(f.read())

    def get_most_recent_run_num(self, archive_path):
        """
        Look in the archive directory to find which build this is. 
        """

        dirs = glob.glob(archive_path + '/output*')
        dirs.sort()

        return int(dirs[-1][-3:])


    def do_basic_access_run(self, exp, model='cm'):

        paths = self.make_paths(exp)
        ret, qso, qse, qsub_files = self.run(paths['exp'], self.lab_path)
        if ret != 0:
            self.print_output([qso, qse, paths['stdout_runtime'], paths['stderr_runtime']])
        print('Run {} failed with code {}.'.format(exp, ret), file=sys.stderr)
        assert(ret == 0)

        run_num = self.get_most_recent_run_num(paths['archive'])
        paths = self.make_paths(exp, run_num)

        # Model output should exist.
        assert(os.path.exists(paths['output']))
        assert(os.path.exists(paths['restart']))
        assert(os.path.exists(paths['stdout']))
        assert(os.path.exists(paths['stderr']))

        with open(paths['stdout'], 'r') as f:
            s = f.read()
            assert('MOM4: --- completed ---' in s)
            if model == 'om':
                assert('********** End of MATM **********' in s)


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
            print('Error: call to payu-run failed.', file=sys.stderr)
            return 1, None, None, None

        self.my_lock.release()

        self.wait(run_id)
        run_id = run_id.split('.')[0]

        output_files = []
        # Read qsub stdout file
        stdout_filename = glob.glob(os.path.join(expt_path,
                                                '*.o{}'.format(run_id)))
        if len(stdout_filename) != 1:
            print('Error: there are too many stdout files.', file=sys.stderr)
            return 2, None, None, None

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
        m = re.search(r'(\d{7}.r-man2)\n', stdout)
        if m is None:
            print('Error: qsub id of collate job.', file=sys.stderr)
            return 3, stdout, stderr, output_files

        # Wait for the collate to complete.
        run_id = m.group(1)
        self.wait(run_id)

        # Return files created by qsub so caller can read or delete.
        collate_files = os.path.join(expt_path, '*.[oe]{}'.format(run_id))
        output_files += glob.glob(collate_files)

        return 0, stdout, stderr, output_files
