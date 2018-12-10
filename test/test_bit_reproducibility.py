
from exp_test_helper import ExpTestHelper, setup_exp_from_base

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
        return l

    @pytest.mark.slow
    def test_bit_repro_repeat(self):
        """
        Test that a run reproduces saved checksums.
        """

        exp_bit_repo1 = setup_exp_from_base('1deg_jra55_iaf', '1deg_jra55_iaf_bit_repo1')
        exp_bit_repo2 = setup_exp_from_base('1deg_jra55_iaf', '1deg_jra55_iaf_bit_repo2')

        # Reconfigure to a 1 day and do run
        for exp in [exp_bit_repo1, exp_bit_repo2]:
            with open(exp.accessom2_config) as f:
                nml = f90nml.read(f)

            nml['date_manager_nml']['restart_period'] = [0, 0, 86400]
            nml.write(exp.accessom2_config, force=True)
            exp.build_and_run()

        # Compare expected to produced.
        assert os.path.exists(exp_bit_repo1.accessom2_out_000)
        expected = self.checksums_to_list(exp_bit_repo1.accessom2_out_000)
        expected.sort()

        assert os.path.exists(exp_bit_repo2.accessom2_out_000)
        produced = self.checksums_to_list(exp_bit_repo2.accessom2_out_000)
        produced.sort()

        if produced != expected:
            with open('checksums-produced-test_bit_repo.txt', 'w') as f:
                f.write('\n'.join(produced))
            with open('checksums-expected-test_bit_repo.txt', 'w') as f:
                f.write('\n'.join(expected))

        assert len(produced) > 0
        assert len(produced) == len(expected)
        assert produced == expected

    @pytest.mark.slow
    def test_bit_repro_historical(self):
        """
        Test that a run reproduces saved checksums.
        """

        exp_bit_repo = setup_exp_from_base('1deg_jra55_iaf', '1deg_jra55_iaf_bit_repo')

        # Reconfigure to a 1 day and do run
        with open(exp_bit_repo.accessom2_config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [0, 0, 86400]
        nml.write(exp_bit_repo.accessom2_config, force=True)
        exp_bit_repo.build_and_run()

        assert os.path.exists(exp_bit_repo.accessom2_out_000)
        produced = self.checksums_to_list(exp_bit_repo.accessom2_out_000)

        # Compare expected to produced.
        test_stdout = os.path.join(exp_bit_repo.exp_path, 'test', 'access-om2.out')
        assert os.path.exists(test_stdout)
        expected = self.checksums_to_list(test_stdout)

        assert len(produced) > 0
        for line in produced:
            if line not in expected:
                with open('checksums-produced-test_bit_repo.txt', 'w') as f:
                    f.write('\n'.join(produced))
                with open('checksums-expected-test_bit_repo.txt', 'w') as f:
                    f.write('\n'.join(expected))


    @pytest.mark.fast
    def test_restart_repro(self):
        """
        Test that a run reproduces across restarts.
        """

        # First do two short (1 day) runs.
        exp_2x1day = setup_exp_from_base('1deg_jra55_iaf', '1deg_jra55_iaf_2x1day')

        # Reconfigure to a 1 day run.
        with open(exp_2x1day.accessom2_config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [0, 0, 86400]
        nml.write(exp_2x1day.accessom2_config, force=True)

        # Don't use Redsea fix - this breaks reproducibility
        # https://github.com/OceansAus/access-om2/issues/124
        with open(exp_2x1day.ocean_config) as f:
            nml = f90nml.read(f)

        nml['auscom_ice_nml']['redsea_gulfbay_sfix'] = False
        nml.write(exp_2x1day.ocean_config, force=True)

        # Now run twice.
        exp_2x1day.build_and_run()
        exp_2x1day.force_run()

        # Now do a single 2 day run
        exp_2day = setup_exp_from_base('1deg_jra55_iaf', '1deg_jra55_iaf_2day')
        # Reconfigure
        with open(exp_2day.accessom2_config) as f:
            nml = f90nml.read(f)

        nml['date_manager_nml']['restart_period'] = [0, 0, 172800]
        nml.write(exp_2day.accessom2_config, force=True)

        # Don't use Redsea fix - this breaks reproducibility
        # https://github.com/OceansAus/access-om2/issues/124
        with open(exp_2day.ocean_config) as f:
            nml = f90nml.read(f)

        nml['auscom_ice_nml']['redsea_gulfbay_sfix'] = False
        nml.write(exp_2day.ocean_config, force=True)

        # Run once.
        exp_2day.build_and_run()

        # Now compare the output between our two short and one long run.
        two_shrt = self.checksums_to_list(exp_2x1day.accessom2_out_000)
        two_shrt = two_shrt + self.checksums_to_list(exp_2x1day.accessom2_out_001)

        one_long = self.checksums_to_list(exp_2day.accessom2_out_000)

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
