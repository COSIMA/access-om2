
from __future__ import print_function

import shutil
import os

from exp_test_helper import ExpTestHelper

tests = {'om_360x300-valgrind': ('om'),
         'om_1440x1080-valgrind': ('om')}


class TestValgrind(ExpTestHelper):
    """
    Run the model in valgrind.
    """

    def __init__(self):
        super(TestValgrind, self).__init__()

    def pre_run_cleanup(self, exp):

        paths = self.make_paths(exp)

        try:
            shutil.rmtree(paths['archive'])
            os.remove(paths['archive_link'])
        except OSError as e:
            if not e.strerror == 'No such file or directory':
                raise e

    def check_run(self, key):

        print('############ Running {} ############'.format(key))
        self.pre_run_cleanup(key)
        self.do_basic_access_run(key, model=tests[key][0])

        # FIXME: check that valgrind does not find any problems.

    def test_runs(self):
        for k in tests.keys():
            yield self.check_run, k
