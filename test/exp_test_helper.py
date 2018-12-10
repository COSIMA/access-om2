
from __future__ import print_function

import subprocess as sp
import sys
import stat
import shutil
import re
import os
import sys
import glob
import time
import yaml

from util import wait_for_qsub, get_git_hash

class ExpTestHelper(object):

    def __init__(self, exp_name, bin_path=None):

        self.exp_name = exp_name
        self.res = exp_name.split('deg')[0].split('_')[-1] + 'deg'

        self.my_path = os.path.dirname(os.path.realpath(__file__))
        self.lab_path = os.path.realpath(os.path.join(self.my_path, '../'))
        if not bin_path:
            self.bin_path = os.path.join(self.lab_path, 'bin')
        else:
            self.bin_path = bin_path
        self.control_path = os.path.join(self.lab_path, 'control')
        self.exp_path = os.path.join(self.control_path, exp_name)
        self.payu_config = os.path.join(self.exp_path, 'config.yaml')
        self.accessom2_config = os.path.join(self.exp_path, 'accessom2.nml')
        self.ocean_config = os.path.join(self.exp_path, 'ocean', 'input.nml')
        self.archive = os.path.join(self.lab_path, 'archive', exp_name)
        self.output000 = os.path.join(self.archive, 'output000')
        self.output001 = os.path.join(self.archive, 'output001')
        self.accessom2_out_000 = os.path.join(self.output000, 'access-om2.out')
        self.accessom2_out_001 = os.path.join(self.output001, 'access-om2.out')

        self.src = os.path.join(self.lab_path, 'src')

        self.libaccessom2_src = os.path.join(self.src, 'libaccessom2')
        self.mom_src = os.path.join(self.src, 'mom')
        self.cice_src = os.path.join(self.src, 'cice5')
        self.yatm_exe = None
        self.mom_exe = None
        self.cice_exe = None
        self.input_path = '/short/public/access-om2/input_rc'

        if not os.path.exists(self.bin_path):
            os.mkdir(self.bin_path)

    def has_run(self):
        """
        See wether this experiment has been run.
        """

        return os.path.exists(os.path.join(self.output000, 'access-om2.out'))

    def make_paths(self, exp_name, run_num=0):
        paths = {}
        run_num = str(run_num).zfill(3)

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

    def setup_for_programmatic_run(self, exes):
        """
        Various config.yaml settings need to be modified in order to run in the
        test environment.
        """

        yatm_exe, cice_exe, mom_exe = exes

        with open(self.payu_config) as f:
            doc = yaml.load(f)

        doc['submodels'][0]['exe'] = yatm_exe
        doc['submodels'][1]['exe'] = mom_exe
        doc['submodels'][2]['exe'] = cice_exe
        doc['runlog'] = False

        with open(self.payu_config, 'w') as f:
            yaml.dump(doc, f)

    def do_basic_access_run(self, exp, model='cm'):
        paths = self.make_paths(exp)
        ret, qso, qse, qsub_files = self.run(paths['exp'], self.lab_path)
        if ret != 0:
            self.print_output([qso, qse,
                               paths['stdout_runtime'],
                               paths['stderr_runtime']])
            fstring = 'Run {} failed with code {}.'
            print(fstring.format(exp, ret), file=sys.stderr)
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

    def copy_to_bin(self, src_dir, wildcard):
        exes = glob.glob(wildcard)
        if len(exes) != 1:
            return None, 1
        exe = exes[0]

        ghash = get_git_hash(src_dir)

        eb = os.path.basename(exe)
        new_name = '{}_{}.{}'.format(eb.split('.')[0], ghash,
                                     eb.split('.')[1])
        dest = os.path.join(self.bin_path, new_name)
        if os.path.exists(dest):
            os.remove(dest)

        shutil.copy(exe, dest)
        shutil.chown(dest, group='v45')
        perms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH  | stat.S_IXUSR \
                 | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(dest, perms)

        return dest, 0


    def build_libaccessom2(self, clean=False):
        """
        Note: the 'clean' arg does nothing. 
        """

        r1 = sp.call([os.path.join(self.libaccessom2_src, 'build_on_raijin.sh')])
        exename, r2 = self.copy_to_bin(self.libaccessom2_src,
                                       self.libaccessom2_src + '/build/bin/yatm.exe')
        return exename, r1 + r2

    def build_cice(self, clean=False):
        os.environ['ACCESS_OM_DIR'] = os.path.join(self.lab_path)
        os.environ['LIBACCESSOM2_ROOT'] = os.path.join(self.libaccessom2_src)
        if clean:
            r1 = sp.call(['make', '-C', self.cice_src, 'clean'])
        r1 = sp.call(['make', '-C', self.cice_src, self.res])

        if self.res == '025deg':
            exe_res = '1440x1080'
        elif self.res == '01deg':
            exe_res = '3600x2700'
        elif self.res == '1deg':
            exe_res = '360x300'
        else:
            assert False

        build_dir_wildcard = self.cice_src + '/build_*_' + exe_res + '_*p/*.exe'
        exename, r2 = self.copy_to_bin(self.cice_src, build_dir_wildcard)

        return exename, r1 + r2

    def build_mom(self, clean=False):
        """
        Note: the 'clean' arg does nothing. 
        """

        os.environ['ACCESS_OM_DIR'] = os.path.join(self.lab_path)
        os.environ['LIBACCESSOM2_ROOT'] = os.path.join(self.libaccessom2_src)

        mydir = os.getcwd()
        os.chdir(os.path.join(self.mom_src, 'exp'))
        r1 = sp.call(['./MOM_compile.csh', '--type', 'ACCESS-OM',
                      '--platform', 'nci', '--repro'])
        os.chdir(mydir)

        exename, r2 = self.copy_to_bin(self.mom_src,
                                        self.mom_src + '/exec/nci/ACCESS-OM/*.x')
        return exename, r1 + r2

    def build(self, clean=False):

        self.yatm_exe, r1 = self.build_libaccessom2(clean)
        if r1 != 0:
            print('YATM build failed for exp {}'.format(self.exp_name),
                  file=sys.stderr)
            return r1
        self.cice_exe, r2 = self.build_cice(clean)
        if r2 != 0:
            print('CICE build failed for exp {}'.format(self.exp_name),
                  file=sys.stderr)

        self.mom_exe, r3 = self.build_mom(clean)
        if r3 != 0:
            print('MOM build failed for exp {}'.format(self.exp_name),
                  file=sys.stderr)

        return [self.yatm_exe, self.cice_exe, self.mom_exe], r1 + r2 + r3

    def run(self):
        """
        Run the experiment using payu and check output.

        Don't do any work if it has already run.
        """

        if self.has_run():
            return 0, None, None, None
        else:
            return self.force_run()

    def force_qsub_run(self):
        """
        Run using qsub
        """

        # Change to experiment directory and run.
        try:
            os.chdir(self.exp_path)
            sp.check_output(['payu', 'sweep', '--lab', self.lab_path])
            run_id = sp.check_output(['payu', 'run', '--lab', self.lab_path])
            run_id = run_id.decode().splitlines()[0]
            os.chdir(self.my_path)
        except sp.CalledProcessError as err:
            os.chdir(self.my_path)
            print('Error: call to payu run failed.', file=sys.stderr)
            return 1, None, None, None

        wait_for_qsub(run_id)
        run_id = run_id.split('.')[0]

        output_files = []
        # Read qsub stdout file
        stdout_filename = glob.glob(os.path.join(self.exp_path,
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
        stderr_filename = glob.glob(os.path.join(self.exp_path,
                                                 '*.e{}'.format(run_id)))
        stderr = ''
        if len(stderr_filename) == 1:
            stderr_filename = stderr_filename[0]
            output_files.append(stderr_filename)
            with open(stderr_filename, 'r') as f:
                stderr = f.read()

        # Read the qsub id of the collate job from the stdout.
        # Payu puts this here.
        m = re.search(r'(\d+.r-man2)\n', stdout)
        if m is None:
            print('Error: qsub id of collate job.', file=sys.stderr)
            return 3, stdout, stderr, output_files

        # Wait for the collate to complete.
        run_id = m.group(1)
        wait_for_qsub(run_id)

        # Return files created by qsub so caller can read or delete.
        collate_files = os.path.join(self.exp_path, '*.[oe]{}'.format(run_id))
        output_files += glob.glob(collate_files)

        return 0, stdout, stderr, output_files

    def force_interactive_run(self):
        """
        Already in a PBS session, run interactively
        """

        # Change to experiment directory and run.
        try:
            os.chdir(self.exp_path)
            sp.check_output(['payu', 'sweep', '--lab', self.lab_path])
            sp.check_output(['payu-run', '--lab', self.lab_path])
        except sp.CalledProcessError as err:
            os.chdir(self.my_path)
            print('Error: call to payu run failed.', file=sys.stderr)
            return 1, None, None, None

        return 0, None, None, None

    def force_run(self):
        """
        Always try to run.
        """

        try:
            dont_care = os.environ['PBS_NODEFILE']
            is_interactive = True
        except:
            is_interactive = False

        # Check whether this is an interactive PBS session.
        if is_interactive:
            ret, stdout, stderr, output_files = self.force_interactive_run()
        else:
            ret, stdout, stderr, output_files = self.force_qsub_run()

        return ret, stdout, stderr, output_files


    def build_and_run(self):

        exes, ret = self.build()
        assert ret == 0
        self.setup_for_programmatic_run(exes)
        self.force_run()


def setup_exp_from_base(base_exp_name, new_exp_name):
    """
    Create a new exp by copying the base config
    """

    base_exp = ExpTestHelper(base_exp_name)

    new_exp_path = os.path.join(base_exp.control_path, new_exp_name)
    if os.path.exists(new_exp_path):
        shutil.rmtree(new_exp_path)
    shutil.copytree(base_exp.exp_path, new_exp_path, symlinks=True)

    new_exp = ExpTestHelper(new_exp_name)
    if os.path.exists(new_exp.archive):
        shutil.rmtree(new_exp.archive)

    try:
        os.remove(os.path.join(new_exp.control_path, 'archive'))
    except OSError:
        pass
    try:
        os.remove(os.path.join(new_exp.control_path, 'work'))
    except OSError:
        pass

    return new_exp


def run_exp(exp_name, force=False):
    my_path = os.path.dirname(os.path.realpath(__file__))

    helper = ExpTestHelper(exp_name)
    exes, ret = helper.build()
    assert ret == 0
    helper.setup_for_programmatic_run(exes)

    if force:
        ret, qso, qse, qsub_files = helper.force_run()
    else:
        ret, qso, qse, qsub_files = helper.run()

    assert ret == 0

    return helper
