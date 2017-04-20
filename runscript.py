#!/usr/bin/env python

import os, sys
import re
import stat
import shutil
import argparse
import subprocess as sp
import glob
import datetime as dt
import netCDF4 as nc
from jinja2 import Template

exp_defs = {'1deg'  : {'ocn_pes' : 120, 'ice_pes' : 6, 'atm_pes' : 1,
                       'res' : '360x300', 'timestep' : 1800},
            '01deg' : {'ocn_pes' : 120, 'ice_pes' : 6, 'atm_pes' : 1,
                       'res' : '3600x2700', 'timestep' : 150 }}

def run(exp, top_dir):
    """
    Run the experiment.
    """

    exp_def = exp_defs[exp]
    ocn_exe = os.path.join(top_dir, 'src/mom/exec/nci/ACCESS-OM/fms_ACCESS-OM.x')

    cice_build = 'auscom_{}_{}p'.format(exp_def['res'], exp_def['ice_pes'])
    ice_exe = os.path.join(top_dir, 'src/cice5/',
                           'build_{}/cice_{}.exe'.format(cice_build, cice_build))
    atm_exe = os.path.join(top_dir, 'src/matm/build_nt62/matm_nt62.exe')

    cmd = ['mpirun', '--mca', 'orte_base_help_aggregate', '0', '-np',
           str(exp_def['ocn_pes']), ocn_exe, ':', '-np', str(exp_def['ice_pes']),
           ice_exe, ':', '-np', '1', atm_exe]

    os.chdir(os.path.join(top_dir, exp))
    with open('accessom.out', 'w') as fout, open('accessom.err', 'w') as ferr:
        popen = sp.Popen(cmd, stdout=sp.PIPE, stderr=ferr)
        # Write to stdout and to file.
        for line in popen.stdout:
            print(line.decode(), end='')
            fout.write(line.decode())
            fout.flush()

    popen.wait()

    return popen.returncode

def copy_files_around(exp_dir, run_date):

    timestamp = str(run_date).replace(' ', '_')

    # Keep a copy of RESTART for later reference.
    shutil.copytree(os.path.join(exp_dir, 'RESTART'),
                    os.path.join(exp_dir, '{}_RESTART'.format(timestamp)))

    # Move the output dir? Need to do something about the MOM output being
    # overwritten. For now just copy all files in exp directory.
    output_dir = os.path.join(exp_dir, '{}_OUTPUT'.format(timestamp))
    os.mkdir(output_dir)
    for f in glob.glob(os.path.join(exp_dir, './*')):
        if os.path.isfile(f):
            shutil.copy(f, output_dir)

    # Copy contents of RESTART into INPUT ready for the next run.
    # FIXME: is it bad that MOM doesn't start from the RESTART dir?
    for f in glob.glob(os.path.join(exp_dir, 'INPUT/*.res.nc')):
        os.chmod(f, stat.S_IRUSR | stat.S_IWUSR)
    for f in glob.glob(os.path.join(exp_dir, 'RESTART/*')):
        shutil.copy(f, os.path.join(exp_dir, 'INPUT'))


def datetime_to_model_format(date):
    """
    Convert a datetime date to dodgy model format string.
    """

    return str(date.year).zfill(4) + str(date.month).zfill(2) + \
           str(date.day).zfill(2)

def init_namelists(exp_dir, timestep, runtime, curr_date,
                   elapsed_time_in_seconds, run_type):
    """
    Set timestep and runtime of experiment.
    """

    assert run_type == "'initial'" or run_type == "'continue'"

    ice_timestep = timestep
    ocn_timestep = timestep
    atm_timestep = timestep
    ice_ocn_coupling_timestep = timestep
    atm_ice_coupling_timestep = 21600

    runtime_in_seconds = runtime
    runtime_in_months = 0
    runtime_in_days = runtime_in_seconds // 86400
    runtime_in_ice_timesteps = runtime_in_seconds // ice_timestep

    for config_file in glob.glob('{}/templates/*'.format(exp_dir)):
        with open(config_file, 'r') as f:
            template = Template(f.read())
            s = template.render(ice_timestep=ice_timestep,
                                ocn_timestep=ocn_timestep,
                                atm_timestep=atm_timestep,
                                runtime_in_seconds=runtime_in_seconds,
                                runtime_in_months=runtime_in_months,
                                runtime_in_days=runtime_in_days,
                                runtime_in_ice_timesteps=runtime_in_ice_timesteps,
                                ice_ocn_coupling_timestep=ice_ocn_coupling_timestep,
                                atm_ice_coupling_timestep=atm_ice_coupling_timestep,
                                current_date=datetime_to_model_format(curr_date),
                                elapsed_time_in_seconds=elapsed_time_in_seconds,
                                run_type=run_type)

            fname = os.path.basename(config_file)
            with open(os.path.join(exp_dir, fname), 'w') as of:
                of.write(s)

def get_cice_date(exp_dir):
    """
    See what CICE thinks the current date and time is.
    """

    res_file = os.path.join(exp_dir, 'RESTART', 'ice.restart_file')
    if not os.path.exists(res_file):
        return dt.datetime(1, 1, 1), 0

    with open(res_file, 'r') as f:
        s = f.read().strip()

    with nc.Dataset(os.path.join(exp_dir, s)) as f:
        curr_date = dt.datetime(f.nyr, f.month, f.mday, second=f.sec)
        elapsed_seconds = int(f.time)

    return curr_date, elapsed_seconds

def get_mom_date(exp_dir):
    """
    See what MOM thinks the current date and time is.
    """

    res_file = os.path.join(exp_dir, 'RESTART', 'ocean_solo.res')
    if not os.path.exists(res_file):
        return dt.datetime(1, 1, 1), dt.datetime(1, 1, 1), 'noleap'

    with open(res_file, 'r') as f:
        s = f.read()
    m = re.search('\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+Current model time: year, month, day, hour, minute, second', s)
    t = tuple([int(m.group(i)) for i in range(1, 7)])
    curr_date = dt.datetime(*t)

    m = re.search('\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+Model start time:   year, month, day, hour, minute, second', s)
    t = tuple([int(m.group(i)) for i in range(1, 7)])
    init_date = dt.datetime(*t)

    m = re.search('\s+(\d+)\s+\(Calendar: no_calendar=0, thirty_day_months=1, julian=2, gregorian=3, noleap=4\)', s)
    if m.group(1) == '4':
        caltype = 'noleap'
    else:
        caltype = None

    return curr_date, init_date, caltype

def is_continuation_run(exp_dir):
    return os.path.exists(os.path.join(exp_dir, 'RESTART', 'ocean_solo.res'))

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment', default='1deg',
                        help='The experiment to run.')
    parser.add_argument('--model_timestep', type=int, default=-1,
                        help='The ice and ocean timestep in seconds.')
    parser.add_argument('--runtime', type=int, default=86400,
                        help='The per-submit runtime in seconds.')

    args = parser.parse_args()

    if args.model_timestep == -1:
        args.model_timestep = exp_defs[args.experiment]['timestep']

    top_dir = os.path.dirname(os.path.realpath(__file__))
    exp_dir = os.path.join(top_dir, args.experiment)

    mom_curr_date, mom_init_date, mom_caltype = get_mom_date(exp_dir)
    cice_curr_date, cice_elapsed_time_seconds = get_cice_date(exp_dir)
    assert mom_curr_date == cice_curr_date
    assert mom_caltype == 'noleap'

    if is_continuation_run(exp_dir):
        run_type = "'continue'"
    else:
        run_type = "'initial'"

    init_namelists(exp_dir, args.model_timestep, args.runtime, mom_curr_date,
                   cice_elapsed_time_seconds, run_type)
    ret = run(args.experiment, top_dir)

    if ret == 0:
        copy_files_around(exp_dir, mom_curr_date)

    return ret

if __name__ == '__main__':
    sys.exit(main())
