
import os
import time
import subprocess as sp

def wait_for_qsub(run_id):
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


def get_git_hash(src_dir):
    """
    Get the git hash of src_dir.
    """
    mydir = os.getcwd()
    os.chdir(src_dir)
    ghash = sp.check_output(['git', 'rev-parse', 'HEAD'])[:8]
    os.chdir(mydir)

    return ghash
