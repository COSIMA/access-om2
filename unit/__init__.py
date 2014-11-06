
import sys, os
import hashlib
import threading

from model_test_helper import ModelTestHelper

def checksum_all_files(dir):
    # Calculate a checksum of all files in a directory. 

    chksum = ''
    for f in os.listdir(dir):
        file = os.path.join(dir, f) 

        if os.path.isfile(file):
            chksum += hashlib.md5(file).digest()

    return chksum

def run_model(helper, exp):

    paths = helper.make_paths(exp)
    ret, _, _, _ = helper.run(paths['exp'], helper.lab_path) 


def setup():
    """
    Prepare for unit tests.
    """

    helper = ModelTestHelper()

    exps = ['cm_360x300-unit_test', 'om_360x300-unit_test',
            'cm_1440x1080-unit_test', 'om_1440x1080-unit_test']

    do_run = []

    # Build with unit testing enabled.  
    #for e in exps:
    for e in []:
        paths = helper.make_paths(e)

        # Get checksum of all files in bin directory. 
        chksum_orig = checksum_all_files(helper.bin_path)
        ret = helper.build(paths['exp'])
        assert(ret == 0)
        chksum_new = checksum_all_files(helper.bin_path)

        if chksum_orig != chksum_new or True:
            do_run.append(True)
        else:
            do_run.append(False)

    do_run = [True] * len(exps)

    # Run if necessary (in parallel). 
    threads = []
    for e, run in zip(exps, do_run):
        if True:
            t = threading.Thread(target=run_model, args=(helper, e))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    # Check that there are output files. If a run was done these will be new. 
    
