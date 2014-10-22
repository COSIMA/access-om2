
import sys

from model_test_helper import ModelTestHelper

def setup():
    """
    Prepare for unit tests.
    """

    helper = ModelTestHelper()

    # Build and run models with unit testing enabled.  
    exps = ['access-cm_1440x1080-unit_test', 'access-cm-unit_test']
    for e in exps:
        paths = helper.make_paths(e)
        ret = helper.build(paths['exp'])
        assert(ret == 0)
        ret, _, _, _ = helper.run(paths['exp'], helper.lab_path) 
        assert(ret == 0)

    # The dumped files should now all be in place. 
