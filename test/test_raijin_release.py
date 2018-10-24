
from __future__ import print_function

from exp_test_helper import ExpTestHelper
import os
import sys
import re
import shutil
import stat
import distutils.dir_util
import tempfile
import tarfile
import hashlib

EXP_NAMES = ['1deg_jra55_ryf', '1deg_jra55_iaf', '1deg_core_nyf',
             '025deg_jra55_ryf', '025deg_jra55_iaf', '025deg_core2_nyf',
             '01deg_jra55_ryf', '01deg_jra55_iaf',
             'minimal_01deg_jra55_ryf', 'minimal_01deg_jra55_iaf']

def update_payu_config(exp_name, res, payu_config, input_dir, yatm_exe, cice_exe, mom_exe):
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

            m_exe = re.search('^\s*exe:\s+\S+', line)
            m_input = re.search('^\s*input:\s+\S+', line)

            if m_exe:
                assert cur_model
                if cur_model == 'atmosphere':
                    print('      exe: {}'.format(yatm_exe), file=fd)
                elif cur_model == 'ocean':
                    print('      exe: {}'.format(mom_exe), file=fd)
                else:
                    print('      exe: {}'.format(cice_exe), file=fd)
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
                else:
                    cice_input = os.path.join(input_dir, 'cice_{}'.format(res))
                    print('      input: {}'.format(cice_input), file=fd)
            else:
                print(line, file=fd, end='')

    shutil.copy(tmp, payu_config)

def calc_checksum(dirname):
    """
    Calculate the checksum of a whole directory.

    This is done but tarring the directory first to make sure that file names
    and other metadata are included in the checksum.
    """

    _, tmp = tempfile.mkstemp(suffix='.tar')
    with tarfile.open(tmp, "w") as tar:
        tar.add(dirname)

    h = hashlib.md5()

    with open(tmp, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    # Delete tarball now that hash has been calculated.
    os.remove(tmp)

    return h.hexdigest()[:8]

def set_input_perms_recursively(path):

    dirperms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH  | stat.S_IXUSR \
               | stat.S_IXGRP | stat.S_IXOTH
    shutil.chown(path, group='v45')
    os.chmod(path, dirperms)

    for root, dirs, files in os.walk(path):
        for d in dirs:
            dirname = os.path.join(root, d)
            shutil.chown(dirname, group='v45')
            os.chmod(dirname, dirperms)
        for f in files:
            fname = os.path.join(root, f)
            shutil.chown(fname, group='v45')
            perms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
            os.chmod(fname, perms)


def update_input_data():

    input_template = '/short/public/access-om2/input_{}'
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


def test_raijin_release():

    input_dir = update_input_data()

    for exp_name in EXP_NAMES:

        # Build new exes.
        exp = ExpTestHelper(exp_name, bin_path='/short/public/access-om2/bin/')
        exes, ret = exp.build()
        if ret != 0:
            print('Build failed for exp {}'.format(exp_name), file=sys.stderr)
        assert ret == 0

        update_payu_config(exp.exp_name, exp.res, exp.payu_config, input_dir, *exes)
