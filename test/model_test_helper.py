
from __future__ import print_function

import subprocess as sp
import sys
import shutil
import re
import os
import glob
import time

class ExpTestHelper(object):

    def __init__(self, exp_name):

        self.exp_name = exp_name
        self.res = exp_name.split('_')[0]
        self.my_path = os.path.dirname(os.path.realpath(__file__))
        self.lab_path = os.path.join(self.my_path, '../')
        self.bin_path = os.path.join(self.lab_path, 'bin')
        self.exp_path = os.path.join(self.lab_path, 'control', exp)
        self.archive = os.path.join(self.lab_path, 'archive', exp)
        self.src = os.path.join(self.lab_path, 'src')
        self.oasis_src = os.path.join(self.src, 'oasis3-mct')
        self.mom_src = os.path.join(self.src, 'mom')
        self.matm_src = os.path.join(self.src, 'matm')
        self.cice5_src = os.path.join(self.src, 'cice5')

    def has_built(self):
        """
        See wether this experiment has been built.
        """

        exes = glob.glob(self.bin_path, '*.exe')
        exes += glob.glob(self.bin_path, '*.x')



    def has_run(self):
        """
        See wether this experiment has been run.
        """


    def make_paths(self, exp_name, run_num=0):
        paths = {}
        run_num = str(run_num).zfill(3)

        paths['archive'] = 
        paths['archive_link'] = os.path.join(paths['exp'], 'archive')
        paths['output'] = os.path.join(paths['archive'], 'output' + run_num)
        paths['restart'] = os.path.join(paths['archive'], 'restart' + run_num)
        paths['stdout'] = os.path.join(paths['output'], 'access.out')
        paths['stderr'] = os.path.join(paths['output'], 'access.err')

        paths['stdout_runtime'] = os.path.join(paths['exp'], 'access.out')
        paths['stderr_runtime'] = os.path.join(paths['exp'], 'access.err')

        return paths

    def print_output(self, files):

        for file in files:
            if file is not None:
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

    def build_oasis(self):
        return sp.call(['make', '-C', 'src/oasis3-mct'])

    def build_matm(self):
        os.environ['OASIS_ROOT'] = os.path.join(self.oasis_src)
        return sp.call(['make', '-C', 'src/matm'])

    def build_cice5(self)
        os.environ['OASIS_ROOT'] = os.path.join(self.oasis_src)
        return sp.call(['make', '-C', 'src/cic5', 'om', self.res])

    def build_mom(self)
        os.environ['OASIS_ROOT'] = os.path.join(self.oasis_src)
        mydir = os.getcwd()
        os.chdir(self.mom_src, 'exp')
        ret = sp.call(['./MOM_compile.csh', '--type', 'ACCESS-OM',
                       '--platform', 'nci'])
        os.chdir(mydir)
        return ret

    def build(self):

        ret = self.build_oasis()
        if ret != 0:
            return ret
        ret += self.build_matm()
        ret += self.build_cice5()
        ret += self.build_mom()

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
            sp.check_output(['payu', 'sweep'])
            run_id = sp.check_output(['payu', 'run'])
            run_id = run_id.splitlines()[0]
            os.chdir(self.my_path)
        except sp.CalledProcessError as err:
            os.chdir(self.my_path)
            print('Error: call to payu-run failed.', file=sys.stderr)
            return 1, None, None, None

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
