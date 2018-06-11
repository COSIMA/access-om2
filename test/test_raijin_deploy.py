
from __future__ import print_function

from exp_test_helper import ExpTestHelper
import tempfile
import tarfile

EXP_NAMES = ['1deg_jra55_ryf', '1deg_jra55_iaf', '1deg_core_nyf', '025_jra55_ryf', '01_jra55_ryf']

def update_payu_config(input_dir, yatm_exe, cice_exe, mom_exe):
    """
    Set the new input_dirs and exes in payu config.yaml
    """

    tmp = tempfile.mkstemp()

    with open(self.payu_config) as fs, open(tmp, 'r+') as fd:
        cur_model = None
        for line in fs:
            m = re.search('name:\s+(\w+)')
            if m:
                cur_model = m.group(1)

            m_exe = re.search('exe:\s+\w+')
            m_input = re.search('input:\s+\w+')
            if m_exe:
                assert cur_model
                if cur_model == 'atmosphere':
                    print('      exe: {}'.format(self.yatm_exe, file=fd)
                elif cur_model == 'ocean':
                    print('      exe: {}'.format(self.mom_exe, file=fd)
                else:
                    print('      exe: {}'.format(self.cice_exe, file=fd)
            elif m_input:
                assert cur_model
                if cur_model == 'atmosphere':
                    print('      exe: {}'.format(self.yatm_exe, file=fd)
                elif cur_model == 'ocean':
                    print('      exe: {}'.format(self.mom_exe, file=fd)
                else:
                    print('      exe: {}'.format(self.cice_exe, file=fd)
            else:
                print(line, file=fd)

def calc_checksum(dirname):
    """
    Calculate the checksum of a whole directory.

    This is done but tarring the directory first to make sure that file names
    and other metadata are included in the checksum.
    """

    _, tmp = tempfile.mkstemp(suffix='.tar')
    with tarfile.open(tmp, "w") as tar:
        tar.add(dirname)

    h = hashlib.blake2b()

    with open(tmp, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    # Delete tarball
    os.remove(tmp)

    return h.hexdigest()

def set_input_perms_recursively(path):

    for root, dirs, files in os.walk(path):  
        for d in dirs:  
            dirname = os.path.join(root, d)
            shutil.chown(dirname, group='v45')
            perms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH  | stat.S_IXUSR \
                     | stat.S_IXGRP | stat.S_IXOTH 
            os.chmod(dirname, perms)
        for f in files:
            fname = os.path.join(root, f)
            shutil.chown(fname, f), group='v45')
            perms = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
            os.chmod(fname, perms)


def update_input_data():

    input_template = '/short/public/access-om2/input_{}'
    input_rc = input_path.format('rc'))

    checksum = calc_checksum(input_rc)
    input_chksum = input_path.format(checksum)

    # Copy release candidate (rc) to dirctory with checksum
    if not os.path.exists(input_chksum):
        shutil.copytree(input_rc, input_chksum)

        # Fix up permissions.
        set_input_perms_recursively(input_chksum)

    return input_chksum


def test_raijin_deploy(self):

    input_dir = update_input_data()

    for exp_name in exp_names:
        if exp_name is not '1deg_core_nyf']:
            return

        # Build new exes.
        exp = ExpTestHelper(exp_name, bin_path='/short/public/access-om2/bin/')
        exes, ret = exp.build()
        assert ret == 0

        exp.update_payu_config(input_dir, *exes)

