
from exp_test_helper import run_exp

import pytest
import yaml
import shutil
import os
import sys
import re


class TestBitReproducibility():

    def checksums_to_list(self, filename, cpl_chksum=False):
        """
        Look at each line an make a list of checksums
        """

        if cpl_chksum:
            regex = re.compile(r'\[chksum\]\s+.*\s+-?[0-9]+$')
        else:
            regex = re.compile(r'\[chksum\] Ice_ocean_boundary.*\s+-?[0-9]+$')
        l = []
        with open(filename) as f:
            for line in f:
                m = regex.match(line)
                if m is not None:
                    l.append(line)
        l.sort()

        return l

    @pytest.mark.fast
    def test_bit_repro(self):
        """
        Test that a run reproduces saved checksums.
        """

        exp = run_exp('1deg_jra55_ryf')

        # Compare expected to produced.
        mom_chksums = os.path.join(exp.exp_path, 'ocean', 'checksums.txt')
        expected = self.checksums_to_list(mom_chksums)
        stdout = os.path.join(exp.archive, 'output000', 'access-om2.out')
        produced = self.checksums_to_list(stdout)

        assert len(produced) == len(expected)
        assert produced == expected

    @pytest.mark.slow
    def test_restart_repro(self):
        """
        Test that a run reproduces across restarts.
        """

        # First do two short (5 day) runs.
        exp = run_exp('1deg_jra55_ryf')
        exp.force_run()

        # Do a single 10 day run
        # Start by copying experiment and modifying the experiment.
        exp_10day = os.path.join(exp.control_path, '1deg_jra55_ryf_10day')
        if not os.path.exists(exp_10day):
            shutil.copytree(exp.exp_path, exp_10day, symlinks=True)
        try:
            os.remove(os.path.join(exp_10day, 'archive'))
        except OSError:
            pass
        try:
            os.remove(os.path.join(exp_10day, 'work'))
        except OSError:
            pass

        # Change to a 10 day run.
        config = os.path.join(exp_10day, 'config.yaml')
        with open(config) as f:
            doc = yaml.load(f)

        doc['calendar']['runtime']['days'] = 10
        doc['jobname'] = '1deg_jra55_ryf_10day'

        with open(config, 'w') as f:
            yaml.dump(doc, f)

        exp_10day = run_exp('1deg_jra55_ryf_10day')

        # Now compare the output between our two short and one long run.
        stdout0 = os.path.join(exp.archive, 'output000', 'access-om2.out')
        two_shrt = self.checksums_to_list(stdout0, cpl_chksum=True)
        stdout1 = os.path.join(exp.archive, 'output001', 'access-om2.out')
        two_shrt = two_shrt + self.checksums_to_list(stdout1, cpl_chksum=True)
        two_shrt.sort()

        stdout = os.path.join(exp_10day.archive, 'output000', 'access-om2.out')
        one_long = self.checksums_to_list(stdout)

        assert len(two_shrt) == len(one_long)
        assert two_shrt == one_long

        # Additionally check that the temp and salt fields of the final restart
        # are identical
