
from __future__ import print_function

import os
import sys
import re
import shutil
import stat
import argparse
import distutils.dir_util
import tempfile
from calc_input_checksum import calc_checksum

my_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(my_path, '../', 'test'))
from exp_test_helper import ExpTestHelper

EXP_NAMES = ['01deg_jra55_ryf', '01deg_jra55_iaf',
             '1deg_jra55_ryf', '1deg_jra55_iaf',
             '025deg_jra55_ryf', '025deg_jra55_iaf']

def update_payu_config(exp_name, res, payu_config, yatm_exe, cice_exe, mom_exe, input_dir=None):
    """
    Set the new input_dirs and exes in payu config.yaml
    """

    _, tmp = tempfile.mkstemp()

    with open(payu_config) as fs, open(tmp, 'r+') as fd:
        cur_model = None
        for line in fs:
            m = re.search('^[\s-]*name:\s+(\S+)', line)
            if m:
                cur_model = m.group(1)

            if re.search('collate', line):
                cur_model = 'collate'

            m_exe = re.search('^\s*exe:\s+\S+', line)
            if input_dir:
                m_input = re.search('^\s*input:\s+\S+', line)
            else:
                m_input = None

            if m_exe:
                assert cur_model
                if cur_model == 'atmosphere':
                    print('      exe: {}'.format(yatm_exe), file=fd)
                elif cur_model == 'ocean':
                    print('      exe: {}'.format(mom_exe), file=fd)
                elif cur_model == 'ice':
                    print('      exe: {}'.format(cice_exe), file=fd)
                else:
                    print(line, file=fd, end='')
            elif m_input:
                assert cur_model
                if cur_model == 'common':
                    if 'jra55' in exp_name:
                        common_input = os.path.join(input_dir, 'common_{}_{}'.format(res, 'jra55'))
                    else:
                        common_input = os.path.join(input_dir, 'common_{}_{}'.format(res, 'core'))
                    print('input: {}'.format(common_input), file=fd)
                elif cur_model == 'atmosphere':
                    yatm_input = os.path.join(input_dir, 'yatm_{}'.format(res))
                    print('      input: {}'.format(yatm_input), file=fd)
                elif cur_model == 'ocean':
                    mom_input = os.path.join(input_dir, 'mom_{}'.format(res))
                    print('      input: {}'.format(mom_input), file=fd)
                elif cur_model == 'ice':
                    cice_input = os.path.join(input_dir, 'cice_{}'.format(res))
                    print('      input: {}'.format(cice_input), file=fd)
                else:
                    print(line, file=fd, end='')
            else:
                print(line, file=fd, end='')

    shutil.copy(tmp, payu_config)


def set_input_perms_recursively(path):

    dirperms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH  | stat.S_IXUSR \
               | stat.S_IXGRP | stat.S_IXOTH
    shutil.chown(path, group='v45')
    os.chmod(path, dirperms)

    for root, dirs, files in os.walk(path):
        for d in dirs:
            dirname = os.path.join(root, d)
            shutil.chown(dirname, group='ik11')
            os.chmod(dirname, dirperms)
        for f in files:
            fname = os.path.join(root, f)
            shutil.chown(fname, group='ik11')
            perms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
            os.chmod(fname, perms)


def update_input_data():

    input_template = '/g/data/ik11/inputs/access-om2/input_{}'
    input_rc = input_template.format('rc')

    checksum = calc_checksum(input_rc)
    input_chksum = input_template.format(checksum)

    # Copy release candidate (rc) to dirctory with checksum
    if not os.path.exists(input_chksum):
        # For some reason shutil.copytree() doesn't work here.
        distutils.dir_util.copy_tree(input_rc, input_chksum, preserve_symlinks=True)

        # Fix up permissions.
        set_input_perms_recursively(input_chksum)

    return input_chksum


def do_release(update_input_data=False):

    if update_input_data:
        input_dir = update_input_data()
    else:
        input_dir = None

    for exp_name in EXP_NAMES:

        # Build new exes.
        exp = ExpTestHelper(exp_name, bin_path='/g/data/ik11/inputs/access-om2/bin/')
        (yatm_exe, cice_exe, mom_exe), ret = exp.build()
        if ret != 0:
            print('Build failed for exp {}'.format(exp_name), file=sys.stderr)
        assert ret == 0

        update_payu_config(exp.exp_name, exp.res, exp.payu_config, yatm_exe, cice_exe, mom_exe, input_dir)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--update_input', default=False, action='store_true',
                        help='Update experiment input directories as well.')

    args = parser.parse_args()

    do_release(update_input_data=args.update_input)


if __name__ == '__main__':
    sys.exit(main())


