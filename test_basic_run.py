
from __future__ import print_function

from nose.plugins.attrib import attr

from model_test_helper import ModelTestHelper

# FIXME: use a test generator here:
# http://nose.readthedocs.org/en/latest/writing_tests.html

class TestBasicRun(ModelTestHelper):
    """
    Basic runs. Run and check return code.
    """

    def __init__(self):
        super(TestBasicRun, self).__init__()

    def pre_test_cleanup(self, exp):

        paths = self.make_paths(exp)

        try:
            shutil.rmtree(paths['archive'])
            os.remove(paths['archive_link'])
        except OSError, e:
            if not e.strerror == 'No such file or directory':
                raise e


    @attr('fast')
    def test_ACCESS_OM_tiny(self):
        """
        Run a tiny ACCESS-OM experiment.

        Do two runs to check that restart work correctly.
        """

        self.pre_test_cleanup('om_360x300-tiny')
        self.do_basic_access_om_run('om_360x300-tiny')
        self.do_basic_access_om_run('om_360x300-tiny')

    @attr('fast')
    def test_ACCESS_CM_tiny(self):
        """
        Run a tiny ACCESS-CM experiment.
        """

        self.pre_test_cleanup('cm_360x300-tiny')
        self.do_basic_access_cm_run('cm_360x300-tiny')
        self.do_basic_access_cm_run('cm_360x300-tiny')


    @attr('slow')
    def test_ACCESS_OM(self):
        """
        Run the ACCESS-OM experiment.
        """

        self.pre_test_cleanup('om_360x300-system_test')
        self.do_basic_access_om_run('om_360x300-system_test')
        self.do_basic_access_om_run('om_360x300-system_test')


    @attr('slow')
    def test_ACCESS_CM(self):
        """
        Run the ACCESS-CM experiment.
        """

        self.pre_test_cleanup('cm_360x300-system_test')
        self.do_basic_access_cm_run('cm_360x300-system_test')
        self.do_basic_access_cm_run('cm_360x300-system_test')


    @attr('slow')
    def test_ACCESS_OM_1440x1080(self):
        """
        Run the ACCESS-OM_1440x1080 experiment.
        """

        self.pre_test_cleanup('om_1440x1080-system_test')
        self.do_basic_access_om_run('om_1440x1080-system_test')
        self.do_basic_access_om_run('om_1440x1080-system_test')


    @attr('slow')
    def test_ACCESS_CM_1440x1080(self):
        """
        Run the ACCESS-CM_1440x1080 experiment.
        """

        self.pre_test_cleanup('cm_1440x1080-system_test')
        self.do_basic_access_cm_run('cm_1440x1080-system_test')
        self.do_basic_access_cm_run('cm_1440x1080-system_test')
