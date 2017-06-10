
from __future__ import print_function

import shutil
import os

from model_test_helper import ModelTestHelper

tests = {'om_360x300-test' : ('om'),
         'om_1440x1080-test' : ('om')}

class TestBasicRun(ModelTestHelper):
    """
    Basic runs. Run and check return code.
    """

    def __init__(self):
        super(TestBasicRun, self).__init__()

    def pre_run_cleanup(self, exp):

        paths = self.make_paths(exp)

        try:
            shutil.rmtree(paths['archive'])
            os.remove(paths['archive_link'])
        except OSError, e:
            if not e.strerror == 'No such file or directory':
                raise e

    def check_run(self, key):

        print('############ Running {} ############'.format(key))
        self.pre_run_cleanup(key)
        self.do_basic_access_run(key, model=tests[key][0])
        self.do_basic_access_run(key, model=tests[key][0])

    def test_runs(self):
        for k in tests.keys():
            yield self.check_run, k
