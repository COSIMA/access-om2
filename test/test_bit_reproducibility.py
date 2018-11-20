
from exp_test_helper import ExpTestHelper, run_exp

import pytest
import f90nml
import shutil
import os
import sys
import re

class TestBitReproducibility():

    def checksums_to_list(self, filename):
        """
        Look at each line an make a list of checksums
        """

        regex_a = re.compile(r'\[chksum\]\s+.*\s+-?[0-9]+$')
        regex_b = re.compile(r'\[chksum\] Ice_ocean_boundary.*\s+-?[0-9]+$')
        l = []
        with open(filename) as f:
            for line in f:
                m = regex_a.match(line)
                if m:
                    l.append(line)
                else:
                    m = regex_b.match(line)
                    if m:
                        l.append(line)
        l.sort()

        return l

    @pytest.mark.fast
    def test_bit_repro(self):
        """
        Test that a run reproduces saved checksums.
        """

        exp = ExpTestHelper('1deg_jra55_ryf')

        # Compare expected to produced.
        test_stdout = os.path.join(exp.exp_path, 'test', 'access-om2.out')
        assert os.path.exists(test_stdout)
        expected = self.checksums_to_list(test_stdout)

        stdout = os.path.join(exp.archive, 'output000', 'access-om2.out')
        assert os.path.exists(stdout)
        produced = self.checksums_to_list(stdout)

        if produced != expected:
            with open('checksums-produced-test_bit_repo.txt', 'w') as f:
                f.write('\n'.join(produced))
            with open('checksums-expected-test_bit_repo.txt', 'w') as f:
                f.write('\n'.join(expected))

        assert len(produced) > 0
        assert len(produced) == len(expected)
        assert produced == expected

    @pytest.mark.fast
    def test_restart_repro(self):
        """
        Test that a run reproduces across restarts.
        """

        exp_orig = ExpTestHelper('1deg_jra55_iaf')

        # First do two short (1 day) runs.
        exp_2x1day_path = os.path.join(exp_orig.control_path, '1deg_jra55_iaf_2x1day')
        if os.path.exists(exp_2x1day_path):
            shutil.rmtree(exp_2x1day_path)
        archive_path = os.path.join(exp_orig.lab_path, 'archive',
                                    '1deg_jra55_iaf_2x1day')
        if os.path.exists(archive_path):
            shutil.rmtree(archive_path)

        shutil.copytree(exp_orig.exp_path, exp_2x1day_path, symlinks=True)
        try:
            os.remove(os.path.join(exp_2x1day_path, 'archive'))
        except OSError:
            pass
        try:
            os.remove(os.path.join(exp_2x1day_path, 'work'))
        except OSError:
            pass

        # Reconfigure to a 1 day run.
        config = os.path.join(exp_2x1day_path, 'accessom2.nml')
        with open(config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [0, 0, 86400]
        nml.write(config, force=True)

        # Now run twice.
        exp_2x1day = run_exp('1deg_jra55_iaf_2x1day')
        exp_2x1day.force_run()

        # Do a single 2 day run
        exp_2day_path = os.path.join(exp_orig.control_path, '1deg_jra55_iaf_2day')
        if os.path.exists(exp_2day_path):
            shutil.rmtree(exp_2day_path)
        archive_path = os.path.join(exp_orig.lab_path, 'archive',
                                    '1deg_jra55_iaf_2day')
        if os.path.exists(archive_path):
            shutil.rmtree(archive_path)

        shutil.copytree(exp_orig.exp_path, exp_2day_path, symlinks=True)
        try:
            os.remove(os.path.join(exp_2day_path, 'archive'))
        except OSError:
            pass
        try:
            os.remove(os.path.join(exp_2day_path, 'work'))
        except OSError:
            pass

        # Reconfigure
        config = os.path.join(exp_2day_path, 'accessom2.nml')
        with open(config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [0, 0, 172800]
        nml.write(config, force=True)

        # Now run twice.
        exp_2day = run_exp('1deg_jra55_iaf_2day')
        exp_2day.force_run()

        # Now compare the output between our two short and one long run.
        stdout0 = os.path.join(exp_2x1day.archive, 'output000', 'access-om2.out')
        two_shrt = self.checksums_to_list(stdout0)
        stdout1 = os.path.join(exp_2x1day.archive, 'output001', 'access-om2.out')
        two_shrt = two_shrt + self.checksums_to_list(stdout1)

        stdout = os.path.join(exp_2day.archive, 'output000', 'access-om2.out')
        one_long = self.checksums_to_list(stdout)
        
        assert len(one_long) > 0
        for line in one_long:
            if line not in two_shrt:
                with open('checksums-two_short-test_restart_repo.txt', 'w') as f:
                    f.write('\n'.join(two_shrt))
                with open('checksums-one_long-test_restart_repo.txt', 'w') as f:
                    f.write('\n'.join(one_long))
                assert line in two_shrt

        # Additionally check that the temp and salt fields of the final restart
        # are identical
