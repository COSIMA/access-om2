
import sys

from model_test_helper import ModelTestHelper

def setup():
    """
    Prepare for unit tests.
    """

    helper = ModelTestHelper()

    # Build and run models with unit testing enabled.  
    exps = ['cm_1440x1080-unit_test', 'om_1440x1080-unit_test', 'cm-unit_test']
    for e in exps:
        paths = helper.make_paths(e)
        ret = helper.build(paths['exp'])
        assert(ret == 0)
        ret, _, _, _ = helper.run(paths['exp'], helper.lab_path) 

    # Check that there are some dumped files in place. 
